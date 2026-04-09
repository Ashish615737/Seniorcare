import streamlit as st
from streamlit_option_menu import option_menu
import streamlit as st
#import streamlit_authenticator as stauth
#from dependencies import sign_up,fetch_user
from streamlit_lottie import st_lottie
import requests
from twilio.rest import Client

st.set_page_config(page_title="ElderEase",page_icon="🧓",layout="wide")


selected=option_menu(
        menu_title=None,
        options=["Home","About","Login/SignUp"],
        icons=['house','chat-quote','journal-code'],
        default_index=0,
        orientation="horizontal"
    )


def lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def twilio():
    res = requests.get("https://ipinfo.io/")
    data = res.json()

    location = data['ip']
    account_sid = 'ACe79bc87589aa38e28ea5ff5a9cd8ccd2'
    auth_token = '2764dc7e259fa5e96f60ad367d6d03a1'
    client = Client(account_sid,auth_token)
    call = client.calls.create(
        twiml = '<Response><Say>This is an emergency from your house. They are in an emergency situation. They need you immediately</Say></Response>',
        to = '+919966324422',
        from_="+14232181236"
    )
    message = client.messages.create(
        to='+919966324422',
        body=f"This is the IP Address of the Device- {location}",
        from_="+14232181236"
    )

    print(message.sid)
    print(call.sid)


with st.sidebar:
    option_menu(
        menu_title=None,
        options=["ElderEase"],
        icons=['alexa']
    )
    lottie_animation11 = "https://lottie.host/97a2d6de-b047-4e89-9294-5f1e70ae8550/vjDo3tyMZQ.json"
    lottie_json11 = lottie_url(lottie_animation11)
    st_lottie(lottie_json11,key="logo",height=250,width=250)

    st.subheader("- Caring for Seniors, One Click at a Time.🫡")
    st.markdown("\n")
    st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")
    #st.markdown("\n")

    c1,c2,c3 = st.sidebar.columns(3)

    with c2:
        if st.sidebar.button(":red[Emergency]"):
            twilio()


    #############################HOME##############################
if selected == "Home":
    st.title("👴 Welcome to Personal Health Assistant 🧓")
    lottie_animation = "https://lottie.host/1a128bcd-8b39-4798-a776-7d92da3a732b/SLotOXOGpI.json"
    lottie_json = lottie_url(lottie_animation)
    st_lottie(lottie_json, key="welcome")

    st.header("Empowering Seniors for a Better Life")
    st.write("Are you or a loved one looking for support in health and communication? Health Assistant is here to help.")
    st.markdown("- 👵 Stay Healthy: Explore our curated health resources, exercise routines, and dietary tips to maintain your well-being.")
    st.markdown("- 🗣️ Stay Connected: Seamlessly connect with friends and family through our user-friendly communication tools.")
    st.markdown("- 🤗 Simple & Intuitive: Our platform is designed with seniors in mind. Easy to use, no tech hassle.")
    st.markdown("- 🌟 Your Trusted Companion: Count on Health Assistant for guidance, companionship, and assistance.")


    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        list-style-position: inside;
    }
    </style>
    ''', unsafe_allow_html=True)
    st.write("Join us in enhancing the golden years of life. Start your journey today!")




#############################ABOUT##############################
if selected=="About":
    st.title(":blue[About ElderEase]")
    lottie_animation2 ="https://lottie.host/fef086f8-1574-4caf-ba7b-fa7c12ced535/gpPTP1xupV.json"
    lottie_json2 = lottie_url(lottie_animation2)
    st_lottie(lottie_json2,key="about us")
    st.header("Empowering Seniors for a Better Life")
    st.markdown("At ElderEase, we believe that every stage of life should be cherished, especially the golden years. Our mission is to empower seniors to live healthier, happier, and more connected lives.")
    st.subheader("Who We Are:")
    st.markdown("ElderEase was founded by a group of passionate individuals who recognized the unique challenges faced by seniors in today's fast-paced world. With backgrounds in healthcare, technology, and senior care, our team is dedicated to making a positive impact on the lives of elders.")
    st.subheader("Our Vision:")
    st.markdown("We envision a world where seniors have easy access to the tools and resources they need to age gracefully and maintain strong connections with their loved ones.")
    st.subheader("What We Offer:")
    st.markdown(
        "-Health and Wellness: Discover a wealth of resources, articles, and exercise routines tailored to senior health. We're here to help you lead an active and healthy lifestyle. ")
    st.markdown(
        "- Communication Made Simple: Our user-friendly communication tools make it effortless to stay in touch with family and friends, no matter where they are.")
    st.markdown("- Tech for All Ages: We're committed to making technology accessible to everyone. Our platform is designed with seniors' needs in mind, ensuring a smooth and frustration-free experience.")

    st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            list-style-position: inside;
        }
        </style>
        ''', unsafe_allow_html=True)
    st.subheader("Join Our Community:")
    st.markdown("ElderEase is more than just a platform; it's a community. Join us today and be part of a growing network of seniors and caregivers who are embracing technology to enhance their lives.")
    st.markdown("Thank you for choosing Personal Health Assistant. Together, we're redefining the way seniors experience the world.")
    st.markdown("\n")
    st.markdown("\n")

if selected=="Login/SignUp":
    import streamlit as st
    import firebase_admin
    from firebase_admin import firestore, credentials, auth
    import json
    import requests
    from streamlit_option_menu import option_menu
    import streamlit_lottie
    from twilio.rest import Client

    # Initialize Firebase if not already initialized
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("elderease-97e9f-48f73342c241.json")
        firebase_admin.initialize_app(cred)


    def load_lottie_animation():
        """Load Lottie animation from URL"""
        animation_url = "https://assets4.lottiefiles.com/packages/lf20_5tl1xxnz.json"
        try:
            r = requests.get(animation_url)
            if r.status_code == 200:
                return r.json()
        except:
            return None


    def app():

        # Custom CSS
        st.markdown("""
            <style>
            .main {
                padding: 2rem;
            }
            .stButton > button {
                width: 100%;
                border-radius: 20px;
                height: 3em;
                background-color: #7E57C2;
                color: white;
                font-weight: bold;
            }
            .stTextInput > div > div > input {
                border-radius: 10px;
            }
            div[data-testid="stForm"] {
                background-color: #f8f9fa;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #7E57C2;
                font-size: 3em;
                text-align: center;
                margin-bottom: 1em;
            }
            .subtitle {
                font-size: 1.2em;
                color: #666;
                text-align: center;
                margin-bottom: 2em;
            }
            </style>
        """, unsafe_allow_html=True)

        # Initialize session states
        for key in ['username', 'useremail', 'signedout', 'signout']:
            if key not in st.session_state:
                st.session_state[key] = '' if key in ['username', 'useremail'] else False

        # Main layout


            # Load and display Lottie animation
            lottie_animation = load_lottie_animation()
            if lottie_animation:
                streamlit_lottie.st_lottie(
                    lottie_animation,
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="low",
                    height=200,
                    key="healthly"
                )

            if not st.session_state["signedout"]:
                tabs = st.tabs(["Login", "Sign Up"])

                with tabs[0]:  # Login tab
                    with st.form("login_form"):
                        st.markdown("##### Welcome Back! 👋")
                        email = st.text_input('Email Address',
                                              placeholder="Enter your email")
                        password = st.text_input('Password',
                                                 type='password',
                                                 placeholder="Enter your password")

                        st.session_state.email_input = email
                        st.session_state.password_input = password

                        col1, col2 = st.columns(2)
                        with col1:
                            submit_login = st.form_submit_button('Login')
                            if submit_login:
                                handle_login()
                        with col2:
                            forgot_password = st.form_submit_button('Forgot Password?')
                            if forgot_password:
                                handle_password_reset()

                with tabs[1]:  # Sign Up tab
                    with st.form("signup_form"):
                        st.markdown("##### Create New Account 📝")
                        new_email = st.text_input('Email Address',
                                                  placeholder="Enter your email")
                        new_username = st.text_input("Username",
                                                     placeholder="Choose a username")
                        new_password = st.text_input('Password',
                                                     type='password',
                                                     placeholder="Create a strong password")

                        submit_signup = st.form_submit_button('Create Account')
                        if submit_signup:
                            if new_email and new_username and new_password:
                                user = sign_up_with_email_and_password(
                                    email=new_email,
                                    password=new_password,
                                    username=new_username
                                )
                                if user:
                                    st.success('Account created successfully! 🎉')
                                    st.markdown('Please login using your email and password')
                                    st.balloons()
                            else:
                                st.error("Please fill in all fields")

            if st.session_state.signout:
                with st.sidebar:
                    with st.sidebar:
                        choices = option_menu(
                            menu_title=None,
                            options=["Elderly Care", "Health Assistant", "PhysioTherapy", "Reminders", "Event Manager",
                                     "Health Guide"],
                            icons=['person-circle', 'alexa', 'activity', 'bell', 'calendar', 'book'],
                            default_index=0,
                            orientation="vertical"
                        )

                    st.markdown("### Welcome to ElderEase")
                    st.markdown(f"**User:** {st.session_state.username}")
                    st.markdown(f"**Email:** {st.session_state.useremail}")
                    if st.button('Sign out', key='signout_button'):
                        handle_signout()

                #write Code here
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.title('🌟 Personalized Health Assistant')
                    st.markdown('<p class="subtitle">Your Personalized Health Assistant for Elderly Care</p>',
                                unsafe_allow_html=True)



    def sign_up_with_email_and_password(email, password, username=None):
        """Handle user sign up"""
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            if username:
                payload["displayName"] = username

            r = requests.post(
                rest_api_url,
                params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"},
                data=json.dumps(payload)
            )

            if r.status_code == 200:
                return r.json().get('email')
            else:
                st.error(f"Signup failed: {r.json().get('error', {}).get('message')}")
                return None
        except Exception as e:
            st.error(f'Signup failed: {str(e)}')
            return None


    def sign_in_with_email_and_password(email, password):
        """Handle user sign in"""
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            r = requests.post(
                rest_api_url,
                params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"},
                data=json.dumps(payload)
            )

            if r.status_code == 200:
                data = r.json()
                return {
                    'email': data['email'],
                    'username': data.get('displayName', 'User')
                }
            else:
                st.error(f"Login failed: {r.json().get('error', {}).get('message')}")
                return None
        except Exception as e:
            st.error(f'Login failed: {str(e)}')
            return None


    def reset_password(email):
        """Handle password reset"""
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            r = requests.post(
                rest_api_url,
                params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"},
                data=json.dumps(payload)
            )
            return r.status_code == 200, "Reset email sent successfully" if r.status_code == 200 else r.json().get(
                'error',
                {}).get(
                'message')
        except Exception as e:
            return False, str(e)


    def handle_login():
        """Handle login form submission"""
        try:
            userinfo = sign_in_with_email_and_password(
                st.session_state.email_input,
                st.session_state.password_input
            )
            if userinfo:
                st.session_state.username = userinfo['username']
                st.session_state.useremail = userinfo['email']
                st.session_state.signedout = True
                st.session_state.signout = True
                st.rerun()
        except Exception as e:
            st.error('Login Failed')


    def handle_signout():
        """Handle sign out"""
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.rerun()


    def handle_password_reset():
        """Handle password reset form"""
        st.markdown("### Password Reset")
        email = st.text_input('Enter your email address')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully!")
            else:
                st.error(f"Password reset failed: {message}")


    if __name__ == "__main__":
        app()