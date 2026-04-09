import streamlit as st
from datetime import datetime, time, timedelta
from winotify import Notification, audio
import json
import requests
from streamlit_lottie import st_lottie


def load_lottie_url(url: str):
    """
    Load Lottie animation from URL
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def initialize_session_state():
    """
    Initialize session state variables
    """
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'notification_count' not in st.session_state:
        st.session_state.notification_count = 1


def create_notification(notification_time, message):
    """
    Create and configure a Windows notification
    """
    toast = Notification(
        app_id="Medicine Reminder",
        title="Time to take Medicine",
        msg=message,
        duration="long",
        icon=r"C:\Users\kumar\Downloads\Medicine.jpg"
    )
    toast.set_audio(audio.LoopingCall, loop=True)
    toast.add_actions(label="Order Online", launch="https://www.netmeds.com/")
    return toast


def calculate_notification_time(notification_time):
    """
    Calculate time until next notification
    """
    current_datetime = datetime.now()
    target_datetime = datetime.combine(current_datetime.date(), notification_time)

    if target_datetime <= current_datetime:
        target_datetime += timedelta(days=1)

    return target_datetime


def main():
    # Page configuration
    st.set_page_config(
        page_title="Medicine Reminder",
        page_icon="💊",
        layout="centered"
    )

    # Initialize session state
    initialize_session_state()

    # Load Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json"
    lottie_json = load_lottie_url(lottie_url)

    # App header with animation
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("💊 Medicine Reminder")
        st.subheader("Set your medication schedule")
    with col2:
        if lottie_json:
            st_lottie(lottie_json, height=150, key="medicine_animation")

    # Input section
    with st.container():
        st.markdown("### Configure Notifications")
        num_notifications = st.number_input(
            "Number of daily medications:",
            min_value=1,
            max_value=10,
            value=st.session_state.notification_count,
            key="notification_input"
        )

        # Update notification count in session state
        if num_notifications != st.session_state.notification_count:
            st.session_state.notification_count = num_notifications
            st.session_state.notifications = []

        # Notification configuration
        with st.form(key="notification_form"):
            for i in range(num_notifications):
                st.markdown(f"#### Medication {i + 1}")
                col1, col2 = st.columns(2)

                with col1:
                    notification_time = st.time_input(
                        f"Time for Medication {i + 1}",
                        value=time(8 + i, 0) if i < 3 else time(8, 0),
                        key=f"time_{i}"
                    )

                with col2:
                    message = st.text_input(
                        f"Medication Name/Notes",
                        value=f"Take Medication {i + 1}",
                        key=f"message_{i}"
                    )

                st.session_state.notifications.append({
                    "time": notification_time,
                    "message": message
                })

            submit_button = st.form_submit_button(label="Set Reminders")

        # Handle form submission
        if submit_button:
            st.markdown("### Scheduled Reminders")
            for idx, notification in enumerate(st.session_state.notifications):
                notification_time = notification["time"]
                message = notification["message"]
                target_datetime = calculate_notification_time(notification_time)

                # Create and show notification
                toast = create_notification(notification_time, message)
                toast.show()

                # Display confirmation
                st.success(
                    f"✅ Reminder {idx + 1} set for "
                    f"{notification_time.strftime('%I:%M %p')}: {message}"
                )

        # Help section
        with st.expander("ℹ️ How to use"):
            st.markdown("""
                1. Enter the number of medications you need reminders for
                2. Set the time for each medication
                3. Add any specific notes or medication names
                4. Click 'Set Reminders' to activate all notifications
                5. Make sure to keep the app running to receive notifications
                """)


if __name__ == "__main__":
    main()