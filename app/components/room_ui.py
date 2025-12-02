import reflex as rx
from app.states.livekit_state import LiveKitState
from app.components.connection_ui import status_badge
from app.components.participant_ui import participant_list, remote_video_grid


def video_preview() -> rx.Component:
    """Displays a placeholder for the local video preview."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                LiveKitState.camera_active,
                rx.el.div(
                    rx.icon(
                        "camera", class_name="h-12 w-12 text-white opacity-50 mb-2"
                    ),
                    rx.el.p(
                        "Local Camera Active",
                        class_name="text-white font-medium text-sm tracking-wide",
                    ),
                    class_name="flex flex-col items-center justify-center h-full w-full animate-pulse",
                ),
                rx.el.div(
                    rx.icon("camera-off", class_name="h-12 w-12 text-gray-400 mb-2"),
                    rx.el.p(
                        "Camera Off", class_name="text-gray-400 font-medium text-sm"
                    ),
                    class_name="flex flex-col items-center justify-center h-full w-full",
                ),
            ),
            class_name="absolute inset-0 flex items-center justify-center",
        ),
        rx.el.div(
            rx.el.div(class_name="h-3 w-3 rounded-full bg-red-500 animate-pulse mr-2"),
            rx.el.span(
                "LIVE", class_name="text-xs font-bold text-white tracking-wider"
            ),
            class_name=rx.cond(
                LiveKitState.camera_active,
                "absolute top-4 left-4 flex items-center bg-black/50 px-2 py-1 rounded backdrop-blur-sm",
                "hidden",
            ),
        ),
        class_name="relative aspect-video bg-gray-900 rounded-2xl overflow-hidden shadow-lg border border-gray-800",
    )


def ptt_button() -> rx.Component:
    """The Push-to-Talk button component."""
    return rx.el.div(
        rx.el.button(
            rx.cond(
                LiveKitState.is_talking,
                rx.icon("mic", class_name="h-12 w-12 text-white mb-2"),
                rx.icon("mic-off", class_name="h-12 w-12 text-white/70 mb-2"),
            ),
            rx.el.span(
                rx.cond(LiveKitState.is_talking, "TRANSMITTING", "HOLD TO TALK"),
                class_name="text-lg font-bold tracking-widest",
            ),
            on_mouse_down=LiveKitState.start_talking,
            on_mouse_up=LiveKitState.stop_talking,
            on_mouse_leave=LiveKitState.stop_talking,
            class_name=rx.cond(
                LiveKitState.is_talking,
                "w-64 h-64 rounded-full bg-red-600 shadow-[0_0_50px_rgba(220,38,38,0.5)] scale-105 transition-all duration-100 flex flex-col items-center justify-center border-4 border-red-400",
                "w-64 h-64 rounded-full bg-gradient-to-b from-violet-600 to-violet-800 shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-200 flex flex-col items-center justify-center border-b-8 border-violet-900",
            ),
        ),
        class_name="flex justify-center py-8",
    )


def room_view() -> rx.Component:
    """The main room view for connected users."""
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h2("Live Room", class_name="text-xl font-bold text-gray-900"),
                status_badge(),
                class_name="flex items-center gap-4",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-5 w-5 mr-2"),
                "Disconnect",
                on_click=LiveKitState.disconnect_from_room,
                class_name="flex items-center px-4 py-2 rounded-lg text-red-600 hover:bg-red-50 font-medium transition-colors",
            ),
            class_name="flex items-center justify-between w-full max-w-4xl mx-auto px-6 py-4 bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-100",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    video_preview(),
                    remote_video_grid(),
                    rx.el.div(
                        rx.el.h3(
                            "Participants",
                            class_name="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3",
                        ),
                        participant_list(),
                        class_name="mt-6",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                rx.el.div(
                    rx.el.div(
                        ptt_button(),
                        rx.el.p(
                            "Press and hold the button to speak",
                            class_name="text-center text-gray-500 text-sm mt-4",
                        ),
                        class_name="bg-white rounded-3xl border border-gray-200 p-8 shadow-sm flex flex-col items-center justify-center h-full",
                    ),
                    class_name="min-h-[400px]",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full max-w-4xl mx-auto p-6",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="flex flex-col min-h-screen bg-gray-50",
    )