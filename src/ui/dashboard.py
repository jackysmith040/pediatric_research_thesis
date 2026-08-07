from nicegui import ui, app, run
import asyncio
from src.ui.components import (
    page_container, 
    navbar,
    alert_banner,
    stat_card,
    video_feed_card
)
from src.state.telemetry import TelemetryState
from src.engine.detector import Detector

def register_dashboard(state: TelemetryState, detector: Detector):
    @ui.page('/dashboard')
    def dashboard():
        # Update progress bars manually since linear_progress value isn't auto-bound nicely from models
        def update_progress():
            total_p = max(1, state.total_daily_adults + state.total_daily_children)
            p_child.value = state.total_daily_children / total_p
            p_adult.value = state.total_daily_adults / total_p

        ui.timer(1.0, update_progress)

        with page_container():
            with navbar('Clinical Command Center'):
                pass
            
            # The core layout: flex-grow fills screen, overflow-y-auto allows vertical scrolling if needed
            with ui.row().classes('w-full h-full flex-grow p-4 md:p-6 gap-6 items-stretch overflow-y-auto flex-wrap md:flex-nowrap'):
                
                # Left Column (Video)
                with ui.column().classes('flex-[2] h-full relative min-w-[300px]'):
                    with video_feed_card('Outpatient Triage Camera 01'):
                        video = ui.interactive_image('/camera/stream').classes('absolute inset-0 w-full h-full object-cover')
                        ui.run_javascript("document.querySelectorAll('.offline-overlay').forEach(el => el.style.display='none');")

                # Right Column (Telemetry)
                with ui.column().classes('flex-[1] h-full flex flex-col gap-4 overflow-y-auto min-w-[300px]'):
                    alert_banner('Capacity Warning', 'Pediatric load exceeds standard waiting capacity. Consider dispatching additional triage staff.', state, 'overcrowding_alert')
                    
                    with ui.row().classes('w-full justify-between items-center mb-0 mt-2'):
                        ui.label('Real-Time Telemetry').classes('text-2xl font-bold tracking-tight text-white')
                        # Live blip
                        with ui.element('span').classes('flex h-3 w-3 relative'):
                            ui.element('span').classes('animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75')
                            ui.element('span').classes('relative inline-flex rounded-full h-3 w-3 bg-emerald-600')
                    
                    with ui.row().classes('w-full gap-4 flex-nowrap'):
                        with ui.element('div').classes('flex-1'):
                            stat_card('Pediatric', state, 'current_children', is_primary=True)
                        with ui.element('div').classes('flex-1'):
                            stat_card('Adult', state, 'current_adults', is_primary=False)
                    
                    # Daily Aggregates (flex-grow so it pushes the button to the bottom)
                    with ui.column().classes('w-full flex-grow bg-slate-900/60 border border-slate-800 rounded-2xl p-6 relative'):
                        ui.label('Daily Aggregates').classes('text-xs font-semibold text-slate-400 tracking-[0.15em] uppercase mb-4 pb-4 border-b border-slate-800 w-full')
                        
                        with ui.column().classes('w-full gap-2 mb-6'):
                            with ui.row().classes('w-full justify-between items-center text-sm'):
                                ui.label('Total Pediatric Processed').classes('font-medium text-white')
                                ui.label().bind_text_from(state, 'total_daily_children').classes('font-bold tracking-wide text-white')
                            p_child = ui.linear_progress(value=0, color='primary').classes('h-2 rounded-full')
                            
                        with ui.column().classes('w-full gap-2'):
                            with ui.row().classes('w-full justify-between items-center text-sm'):
                                ui.label('Total Adults Processed').classes('font-medium text-slate-400')
                                ui.label().bind_text_from(state, 'total_daily_adults').classes('font-bold tracking-wide text-slate-300')
                            p_adult = ui.linear_progress(value=0, color='grey-6').classes('h-2 rounded-full')
                    
                    # Generate Report Buttons
                    async def generate_csv():
                        btn_csv.props('loading')
                        await asyncio.sleep(0.5)
                        from src.engine import reporter
                        csv_bytes = await run.io_bound(lambda: reporter.generate_csv(state))
                        ui.download.content(csv_bytes, 'capacity_report.csv', media_type='text/csv')
                        btn_csv.props(remove='loading')
                        ui.notify('CSV downloaded successfully.', type='positive')

                    async def generate_pdf():
                        btn_pdf.props('loading')
                        await asyncio.sleep(0.5)
                        from src.engine import reporter
                        pdf_bytes = await run.io_bound(lambda: reporter.generate_pdf(state))
                        ui.download.content(pdf_bytes, 'capacity_report.pdf', media_type='application/pdf')
                        btn_pdf.props(remove='loading')
                        ui.notify('PDF downloaded successfully.', type='positive')

                    with ui.row().classes('w-full gap-2 mt-2'):
                        btn_csv = ui.button('CSV Report', on_click=generate_csv) \
                            .props('outline rounded size=lg icon=table_view') \
                            .classes('flex-1 font-bold border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-colors')
                        btn_pdf = ui.button('PDF Report', on_click=generate_pdf) \
                            .props('outline rounded size=lg icon=picture_as_pdf') \
                            .classes('flex-1 font-bold border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-colors')
