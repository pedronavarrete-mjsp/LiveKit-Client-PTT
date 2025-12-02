import reflex as rx
from app.components.connection_ui import connection_form
from app.components.room_ui import room_view
from app.states.livekit_state import LiveKitState


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            LiveKitState.is_connected,
            room_view(),
            rx.el.main(
                rx.el.div(
                    class_name="absolute inset-0 -z-10 h-full w-full bg-white [background:radial-gradient(125%_125%_at_50%_10%,#fff_40%,#63e_100%)] opacity-20"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "LiveKit Client",
                            class_name="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight mb-2",
                        ),
                        rx.el.p(
                            "Connect to your real-time infrastructure",
                            class_name="text-lg text-gray-600 mb-12",
                        ),
                        class_name="text-center",
                    ),
                    connection_form(),
                    rx.el.footer(
                        rx.el.p(
                            "Phase 2: Local Media & PTT",
                            class_name="text-sm text-gray-400 font-medium",
                        ),
                        class_name="mt-16 text-center",
                    ),
                    class_name="container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-screen",
                ),
                class_name="relative min-h-screen font-['Inter'] text-gray-900",
            ),
        ),
        class_name="min-h-screen bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")