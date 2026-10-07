import random
from datetime import datetime
import streamlit as st

# ====================================================
# 1. 페이지 기본 설정 및 디자인
# ====================================================
st.set_page_config(
    page_title="✨ 오늘의 띠별 운세",
    page_icon="🔮",
    layout="centered",
)

# Custom CSS로 디자인 스타일링
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #4A154B;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    .fortune-box {
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #6B46C1;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .luck-item {
        font-size: 1.05rem;
        font-weight: 600;
        color: #2D3748;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ====================================================
# 2. 띠별 운세 데이터 정의
# ====================================================
ZODIAC_DATA = {
    "쥐띠 🐭": {
        "fortunes": [
            "그동안 준비해 온 일이 성과를 나타내기 시작하는 좋은 날입니다.",
            "주변 사람과의 대화에서 뜻밖의 좋은 아이디어를 얻을 수 있습니다.",
            "차분하게 순서를 지키며 일 처리하면 기대 이상의 결과가 따라옵니다.",
        ],
        "colors": ["보라색", "네이비", "아이보리"],
        "items": ["다이어리", "아메리카노", "텀블러"],
    },
    "소띠 🐮": {
        "fortunes": [
            "성실한 태도가 빛을 발하여 주변의 인정을 받게 되는 날입니다.",
            "새로운 시작을 도모하기에 적합하며 성급함만 주의하면 완벽합니다.",
            "가족이나 가까운 동료와의 대화가 마음의 안정을 가져다줍니다.",
        ],
        "colors": ["노란색", "브라운", "올리브 GREEN"],
        "items": ["손수건", "따뜻한 차", "노트북"],
    },
    "호랑이띠 🐯": {
        "fortunes": [
            "도전 정신이 빛을 발하는 날입니다. 망설이던 일을 실행해 보세요.",
            "리더십을 발휘하면 팀이나 그룹 내에서 좋은 반응을 얻습니다.",
            "금전운이 좋아 뜻밖의 소소한 이득이 생길 수 있습니다.",
        ],
        "colors": ["주황색", "버건디", "골드"],
        "items": ["명함집", "스마트워치", "비타민"],
    },
    "토끼띠 🐰": {
        "fortunes": [
            "원만한 인맥 관계가 유지되며 마음의 평화를 찾는 하루입니다.",
            "세심함과 신중함이 필요한 날로, 서류나 계약 건을 꼼꼼히 챙기세요.",
            "취미 활동이나 휴식을 통해 에너지 충전하기에 가장 좋습니다.",
        ],
        "colors": ["핑크색", "연두색", "화이트"],
        "items": ["핸드크림", "블루투스 이어폰", "꽃 한 송이"],
    },
    "용띠 🐲": {
        "fortunes": [
            "자신감이 넘치고 활력이 샘솟아 무엇이든 해낼 수 있는 날입니다.",
            "귀인을 만나 도움을 받거나 좋은 제안을 들을 수 있습니다.",
            "목표를 높게 설정하고 대범하게 행동하면 성공에 한 걸음 다가섭니다.",
        ],
        "colors": ["붉은색", "골드", "블랙"],
        "items": ["선글라스", "지갑", "에스프레소"],
    },
    "뱀띠 🐍": {
        "fortunes": [
            "통찰력이 예리해져 복잡한 문제를 명쾌하게 해결할 수 있습니다.",
            "지출 관리에 신경 써야 하는 날로, 충동구매를 자제하세요.",
            "조용히 자신의 내실을 다지면 조만간 큰 기회가 올 것입니다.",
        ],
        "colors": ["다크그레이", "에메랄드", "은색"],
        "items": ["책", "볼펜", "미스트"],
    },
    "말띠 🐴": {
        "fortunes": [
            "에너지가 넘치고 기분 좋은 소식이 찾아오는 활기찬 하루입니다.",
            "야외 활동이나 운동을 즐기면 건강과 운이 동시에 상승합니다.",
            "적극적으로 소통하면 애정운과 인간관계가 크게 향상됩니다.",
        ],
        "colors": ["파란색", "하늘색", "코랄"],
        "items": ["운동화", "모자", "이온음료"],
    },
    "양띠 🐑": {
        "fortunes": [
            "부드러운 미소와 친절함이 상대방의 마음을 움직이는 날입니다.",
            "예술적 감수성이나 창의적인 생각이 일에 큰 도움이 됩니다.",
            "주변 사람들에게 베푼 호의가 더 큰 행운으로 돌아옵니다.",
        ],
        "colors": ["베이지", "크림색", "민트"],
        "items": ["쿠션", "향수", "초콜릿"],
    },
    "원숭이띠 🐵": {
        "fortunes": [
            "재치와 임기응변이 뛰어나 위기 상황을 지혜롭게 넘어갑니다.",
            "새로운 정보나 소식을 접하면 빠르게 기회로 포착해 보세요.",
            "즐거운 유머 감각이 주변 환경을 한층 화기애애하게 만듭니다.",
        ],
        "colors": ["노란색", "실버", "라임"],
        "items": ["스마트폰", "간식", "키링"],
    },
    "닭띠 🐔": {
        "fortunes": [
            "시작과 마무리가 완벽하여 일을 깔끔하게 처리하게 되는 날입니다.",
            "약속 시간이나 일정을 철저히 지키면 신뢰도가 급상승합니다.",
            "자기관리에 시간을 투자하면 기분 전환과 운세 상승을 동시에 이룹니다.",
        ],
        "colors": ["하얀색", "골드", "레드"],
        "items": ["탁상시계", "립밤", "거울"],
    },
    "개띠 🐶": {
        "fortunes": [
            "솔직하고 진실된 마음가짐이 주변 사람들에게 신뢰를 줍니다.",
            "오랜 친구나 동료로부터 기분 좋은 연락이 도착할 수 있습니다.",
            "협동하여 하는 일에서 유의미한 성과를 거두는 기분 좋은 하루입니다.",
        ],
        "colors": ["카키색", "브라운", "체리레드"],
        "items": ["키홀더", "매직펜", "우산"],
    },
    "돼지띠 🐷": {
        "fortunes": [
            "마음이 풍요롭고 식복과 재물운이 나란히 따르는 하루입니다.",
            "낙천적인 태도가 복을 불러오니 여유로운 마음을 가지세요.",
            "원하던 목표에 한 걸음 더 다가서는 의미 있는 시간입니다.",
        ],
        "colors": ["분홍색", "청록색", "연보라"],
        "items": ["돼지 저금통", "달콤한 디저트", "상품권"],
    },
}

# ====================================================
# 3. Streamlit 앱 화면 구성
# ====================================================

# 헤더 영역
st.markdown(
    "<div class='main-title'>🔮 오늘의 띠별 운세 🔮</div>",
    unsafe_allow_html=True,
)
today_str = datetime.now().strftime("%Y년 %m월 %d일")
st.markdown(
    f"<div class='sub-title'>{today_str} 기준 오늘의 운세를 확인해 보세요!</div>",
    unsafe_allow_html=True,
)

# 셀렉트박스 (띠 선택)
zodiac_list = list(ZODIAC_DATA.keys())
selected_zodiac = st.selectbox(
    "👉 당신의 띠를 선택하세요:",
    zodiac_list,
    index=0,
)

# 운세 보기 버튼
if st.button("✨ 운세 확인하기", type="primary", use_container_width=True):
    zodiac_info = ZODIAC_DATA[selected_zodiac]

    # 날짜와 띠 조합으로 랜덤 씨드 고정 (하루 동안 같은 운세 유지)
    seed_value = int(datetime.now().strftime("%Y%m%d")) + zodiac_list.index(
        selected_zodiac
    )
    random.seed(seed_value)

    fortune_text = random.choice(zodiac_info["fortunes"])
    lucky_color = random.choice(zodiac_info["colors"])
    lucky_item = random.choice(zodiac_info["items"])
    lucky_number = random.randint(1, 99)

    # 결과 출력
    st.markdown(
        f"""
    <div class='fortune-box'>
        <h3>[{selected_zodiac}] 오늘의 총운</h3>
        <p style='font-size: 1.15rem; line-height: 1.6; color: #1A202C;'>"{fortune_text}"</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")  # 여백

    # 행운 지수 3열 레이아웃
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="🎨 행운의 색상", value=lucky_color)
    with col2:
        st.metric(label="🍀 행운의 아이템", value=lucky_item)
    with col3:
        st.metric(label="🔢 행운의 숫자", value=str(lucky_number))

    st.balloons()  # 축하 애니메이션