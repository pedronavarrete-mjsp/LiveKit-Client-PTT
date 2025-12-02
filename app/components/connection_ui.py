import reflex as rx
from app.states.livekit_state import LiveKitState


def status_badge() -> rx.Component:
    """Displays the current connection status."""
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                LiveKitState.connection_status == "connected",
                "animate-pulse h-2.5 w-2.5 rounded-full bg-emerald-500",
                rx.cond(
                    LiveKitState.connection_status == "connecting",
                    "animate-bounce h-2.5 w-2.5 rounded-full bg-yellow-500",
                    rx.cond(
                        LiveKitState.connection_status == "error",
                        "h-2.5 w-2.5 rounded-full bg-red-500",
                        "h-2.5 w-2.5 rounded-full bg-gray-400",
                    ),
                ),
            )
        ),
        rx.el.span(
            LiveKitState.status_message, class_name="text-sm font-medium text-gray-600"
        ),
        class_name="flex items-center gap-3 px-4 py-3 bg-gray-50 rounded-xl border border-gray-100",
    )


def connection_form() -> rx.Component:
    """The main connection form component."""
    return rx.el.div(
        rx.el.div(
            rx.icon("network", class_name="h-8 w-8 text-violet-600"),
            rx.el.h2(
                "LiveKit Connection", class_name="text-xl font-semibold text-gray-900"
            ),
            class_name="flex items-center gap-3 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "LiveKit URL",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    placeholder="wss://your-project.livekit.cloud",
                    on_change=LiveKitState.set_url,
                    disabled=LiveKitState.is_connected,
                    class_name=rx.cond(
                        LiveKitState.is_connected,
                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed",
                        "w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition-all text-gray-900 placeholder-gray-400",
                    ),
                    default_value=LiveKitState.livekit_url,
                ),
                class_name="mb-5",
            ),
            rx.el.div(
                rx.el.label(
                    "Access Token",
                    class_name="block text-sm font-medium text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    placeholder="ey...",
                    type="password",
                    on_change=LiveKitState.set_token,
                    disabled=LiveKitState.is_connected,
                    class_name=rx.cond(
                        LiveKitState.is_connected,
                        "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed",
                        "w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-violet-500 focus:border-violet-500 transition-all text-gray-900 placeholder-gray-400",
                    ),
                    default_value=LiveKitState.token,
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.cond(
                    LiveKitState.is_connected,
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        "Disconnect",
                        on_click=LiveKitState.disconnect_from_room,
                        class_name="flex items-center justify-center gap-2 w-full px-4 py-2.5 bg-red-50 text-red-600 hover:bg-red-100 border border-red-100 rounded-lg font-medium transition-colors",
                    ),
                    rx.el.button(
                        rx.cond(
                            LiveKitState.is_connecting,
                            rx.el.span(
                                "Connecting...", class_name="flex items-center gap-2"
                            ),
                            rx.el.span(
                                rx.icon("plug", class_name="h-4 w-4"),
                                "Connect to Room",
                                class_name="flex items-center gap-2",
                            ),
                        ),
                        on_click=LiveKitState.connect_to_room,
                        disabled=LiveKitState.is_connecting,
                        class_name=rx.cond(
                            LiveKitState.is_connecting,
                            "w-full px-4 py-2.5 bg-violet-400 text-white rounded-lg font-medium cursor-wait",
                            "w-full px-4 py-2.5 bg-violet-600 hover:bg-violet-700 text-white rounded-lg font-medium transition-colors shadow-sm hover:shadow",
                        ),
                    ),
                )
            ),
            class_name="space-y-1",
        ),
        rx.el.div(status_badge(), class_name="mt-6 pt-6 border-t border-gray-100"),
        class_name="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-gray-200 max-w-md w-full mx-auto",
    )