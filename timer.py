import streamlit as st
import time
#사이트 이름 및 아이콘, 레이아웃 설정
st.set_page_config(
    page_title='위니브 타이머',
    page_icon='⏰',
    layout = 'centered'
)

#st.title('위니브 타이머')
#st.capton('작업 리듬을 만들어주는 음악 타이머')
st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1 style="font-size: 3rem; font-weight: bold;">위니브 타이머</h1>
    <p style="color: #888; font-size: 0.8rem;">작업 리듬을 만들어주는 음악 타이머</p>
</div>
""", unsafe_allow_html=True)

if 'timer_running' not in st.session_state:  #세션스테이트가 없을 때
    st.session_state.timer_running=False
if 'timer_paused' not in st.session_state:  
    st.session_state.timer_paused=False
if 'start_time' not in st.session_state:  
    st.session_state.start_time=None
if 'total_pause_time' not in st.session_state:  
    st.session_state.total_pause_time=0 #none은 계산할 수 없으므로 0
if 'total_seconds' not in st.session_state:  
    st.session_state.total_seconds=25*60 #기본 디폴트값 설정(초단위)
if 'timer_completed' not in st.session_state:  
    st.session_state.timer_completed=False
if 'show_celebration' not in st.session_state:  
    st.session_state.show_celebration=False
if 'remaining_seconds' not in st.session_state:  
    st.session_state.remaining_seconds=25*60

def update_timer(): #타이머 실행중
    if st.session_state.timer_running and not st.session_state.timer_paused: #타이머 실행중이고 타이머 정지버튼을 누르지 않았을 때
        current_time = time.time() #현재 시간
        elapsed = session_state.start_time-st.session_state.total_pause_time #현재시간-시작시간-정지한 시간(=경과시간)
        remaining = st.session_state.total_seconds - int(elapsed)

        if remaining<=0:
            st.session_state.remaining_seconds = 0 #남은 시간
            st.session_state.timer_running = False
            st.session_state.timer_completed = True
            st.session_state.show_celebration = True
        else:
            st.session_state.remaining_seconds = remaining

def get_timer_status():
    #타이머가 완료됐을 때
    if st.session_state.timer_completed:
        return "completed"

    #타이머가 진행중이고, 정지 버튼을 누르지 않았을 때
    elif st.session_state.timer_running and not st.session_state.timer_paused: 
        return "running"
    #타이머 정지 버튼을 눌렀을 때
    elif st.session_state.timer_paused:
        return "paused"
    #그 외
    else:
        return "stopped" #타이머 완전 종료

update_timer()
current_status = get_timer_status() #타이머 진행중일 때의 상태

#메인 레이아웃(2열로 만들기,진행률, 시간초, 설정시간, 경과시간)

col_left, col_right = st.columns(2)

with col_left:
    if st.session_state.total_seconds > 0:
        progress = st.session_state.remaining_seconds/st.session_state.total_seconds #진행률
        progress = max(0,min(1,progress)) #혹시나 결과값이 마이너스가 되지 않게(진행율이 0부터 1사이의 값만 출력되도록 함)
    else:
        progress = 0
    st.progress(float(progress)) #실수 형태로만 들어가게
    
    #타이머가 진행중일때 표현하기
    status_col1,status_col2,status_col3 = st.columns(3)
    with status_col1: #"타이머"
        if current_status=="running":
            st.markdown('타이머',help="타이머가 실행중입니다.")
        elif current_status=="paused":
            st.markdown('타이머',help="타이머가 일시 정지 되었습니다.")
        elif current_status=="completed":
            st.markdown('타이머',help="타이머가 완료되었습니다!")
        else :
            st.markdown('타이머',help="타이머가 대기중입니다.")
    with status_col3: #퍼센트(진행율)
        st.markdown(f"{int(progress*100)%}") #왼쪽정렬이 되기 떄문에


with col_right:
    pass