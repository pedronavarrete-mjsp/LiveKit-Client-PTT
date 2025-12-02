import reflex as rx
from app.states.livekit_state import LiveKitState


def participant_controls(p: dict) -> rx.Component:
    """Controls for a single participant."""
    return rx.el.div(
        rx.el.button(
            rx.cond(
                p["audio_subscribed"],
                rx.icon("mic", class_name="h-4 w-4 text-emerald-600"),
                rx.icon("mic-off", class_name="h-4 w-4 text-gray-400"),
            ),
            on_click=lambda: LiveKitState.toggle_subscription(p["sid"], "audio"),
            disabled=~p["has_audio"],
            class_name=rx.cond(
                p["has_audio"],
                rx.cond(
                    p["audio_subscribed"],
                    "p-2 rounded-lg bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 transition-colors",
                    "p-2 rounded-lg bg-gray-50 hover:bg-gray-100 border border-gray-200 transition-colors",
                ),
                "p-2 rounded-lg bg-gray-50 opacity-50 cursor-not-allowed border border-transparent",
            ),
            title=rx.cond(p["has_audio"], "Toggle Audio", "No Audio Available"),
        ),
        rx.el.button(
            rx.cond(
                p["video_subscribed"],
                rx.icon("video", class_name="h-4 w-4 text-blue-600"),
                rx.icon("video-off", class_name="h-4 w-4 text-gray-400"),
            ),
            on_click=lambda: LiveKitState.toggle_subscription(p["sid"], "video"),
            disabled=~p["has_video"],
            class_name=rx.cond(
                p["has_video"],
                rx.cond(
                    p["video_subscribed"],
                    "p-2 rounded-lg bg-blue-50 hover:bg-blue-100 border border-blue-200 transition-colors",
                    "p-2 rounded-lg bg-gray-50 hover:bg-gray-100 border border-gray-200 transition-colors",
                ),
                "p-2 rounded-lg bg-gray-50 opacity-50 cursor-not-allowed border border-transparent",
            ),
            title=rx.cond(p["has_video"], "Toggle Video", "No Video Available"),
        ),
        class_name="flex items-center gap-2",
    )


def participant_item(p: dict) -> rx.Component:
    """Row item for a single participant."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    p["identity"].to_string()[0].upper(),
                    class_name="text-sm font-bold text-violet-600",
                ),
                class_name="h-8 w-8 rounded-full bg-violet-100 flex items-center justify-center border border-violet-200",
            ),
            rx.el.div(
                rx.el.p(
                    p["identity"],
                    class_name="text-sm font-semibold text-gray-900 truncate max-w-[120px]",
                ),
                rx.el.p(
                    p["sid"],
                    class_name="text-xs text-gray-400 truncate max-w-[120px] font-mono",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-3",
        ),
        participant_controls(p),
        class_name="flex items-center justify-between p-3 rounded-xl bg-white border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def participant_list() -> rx.Component:
    """List of remote participants."""
    return rx.el.div(
        rx.cond(
            LiveKitState.remote_participants.length() > 0,
            rx.el.div(
                rx.foreach(LiveKitState.remote_participants, participant_item),
                class_name="space-y-2",
            ),
            rx.el.div(
                rx.icon("users", class_name="h-8 w-8 text-gray-300 mb-2"),
                rx.el.p(
                    "No other participants",
                    class_name="text-sm font-medium text-gray-400",
                ),
                class_name="flex flex-col items-center justify-center py-8 bg-gray-50 rounded-xl border border-dashed border-gray-200",
            ),
        ),
        class_name="flex flex-col gap-3",
    )


def remote_video_card(p: dict) -> rx.Component:
    """Simulated video feed for a remote participant."""
    return rx.el.div(
        rx.el.div(
            rx.icon("user", class_name="h-16 w-16 text-gray-300 mb-2"),
            rx.el.p(
                p["identity"],
                class_name="text-white font-semibold text-lg shadow-black drop-shadow-md",
            ),
            rx.el.div(
                rx.icon("video", class_name="h-4 w-4 text-white"),
                rx.el.span(
                    "Remote Video", class_name="text-xs font-medium text-white ml-1.5"
                ),
                class_name="flex items-center mt-2 bg-black/30 px-3 py-1 rounded-full backdrop-blur-sm",
            ),
            class_name="absolute inset-0 flex flex-col items-center justify-center",
        ),
        rx.cond(
            p["audio_subscribed"],
            rx.el.div(
                rx.icon("mic", class_name="h-3 w-3 text-white"),
                class_name="absolute top-3 right-3 h-6 w-6 rounded-full bg-emerald-500 flex items-center justify-center shadow-lg",
            ),
        ),
        rx.el.div(
            rx.el.span(
                p["identity"],
                class_name="text-xs font-bold text-white uppercase tracking-wider",
            ),
            class_name="absolute bottom-3 left-3 bg-black/50 px-2 py-1 rounded backdrop-blur-sm",
        ),
        class_name="relative aspect-video bg-gray-800 rounded-2xl overflow-hidden shadow-lg border border-gray-700 animate-in fade-in duration-300",
    )


def remote_video_grid() -> rx.Component:
    """Grid of subscribed remote video streams."""
    return rx.el.div(
        rx.foreach(
            LiveKitState.remote_participants,
            lambda p: rx.cond(
                p["video_subscribed"], remote_video_card(p), rx.fragment()
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full",
    )