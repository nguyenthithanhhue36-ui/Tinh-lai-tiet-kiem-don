# Tinh-lai-tiet-kiem-don
import streamlit as st
import pandas as pd

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Máy tính lãi suất tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# ==============================
# CSS GIAO DIỆN
# ==============================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        text-align: center;
        border: 1px solid #e0e0e0;
    }

    .result-title {
        font-size: 16px;
        color: #555;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 24px;
        font-weight: bold;
    }

    .formula {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="main-title">💰 MÁY TÍNH LÃI SUẤT TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính lãi đơn và lãi kép theo kỳ hạn gửi tiết kiệm</div>',
    unsafe_allow_html=True
)

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP THÔNG TIN
# ==============================
st.subheader("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=1000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    interest_type = st.selectbox(
        "📈 Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    interest_rate = st.number_input(
        "📊 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

with col2:
    term = st.number_input(
        "⏳ Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    payment_type = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )


# ==============================
# NÚT TÍNH TOÁN
# ==============================
st.markdown("---")

calculate = st.button(
    "🧮 TÍNH LÃI",
    use_container_width=True,
    type="primary"
)


# ==============================
# TÍNH TOÁN
# ==============================
if calculate:

    # Kiểm tra dữ liệu
    if principal <= 0:
        st.error("Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if interest_rate < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    annual_rate = interest_rate / 100

    # Số tháng
    months = int(term)

    # ==============================
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # ==============================
    if payment_type == "Lãnh lãi hàng tháng":
        period_months = 1
        number_of_periods = months
        period_name = "Tháng"

    elif payment_type == "Lãnh lãi hàng quý":
        period_months = 3

        # Nếu kỳ hạn không chia hết cho 3
        # thì vẫn tính phần thời gian còn lại
        number_of_periods = (months + 2) // 3
        period_name = "Quý"

    else:
        period_months = months
        number_of_periods = 1
        period_name = "Cuối kỳ"

    # ==============================
    # LÃI ĐƠN
    # ==============================
    if interest_type == "Lãi đơn":

        total_interest = principal * annual_rate * (months / 12)

        final_amount = principal + total_interest

        # Lãi theo tháng
        monthly_interest = principal * annual_rate / 12

        # Tạo bảng chi tiết
        data = []

        accumulated_interest = 0

        if payment_type == "Lãnh lãi hàng tháng":

            for i in range(1, months + 1):

                accumulated_interest += monthly_interest

                data.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền gốc": format_money(principal),
                    "Tiền lãi kỳ này": format_money(monthly_interest),
                    "Lãi tích lũy": format_money(accumulated_interest),
                    "Tổng tiền": format_money(
                        principal + accumulated_interest
                    )
                })

        elif payment_type == "Lãnh lãi hàng quý":

            quarter = 0
            remaining_months = months

            while remaining_months > 0:

                quarter += 1

                current_months = min(3, remaining_months)

                quarter_interest = (
                    principal
                    * annual_rate
                    * current_months
                    / 12
                )

                accumulated_interest += quarter_interest

                data.append({
                    "Kỳ": f"Quý {quarter}",
                    "Tiền gốc": format_money(principal),
                    "Tiền lãi kỳ này": format_money(quarter_interest),
                    "Lãi tích lũy": format_money(accumulated_interest),
                    "Tổng tiền": format_money(
                        principal + accumulated_interest
                    )
                })

                remaining_months -= current_months

        else:

            data.append({
                "Kỳ": "Cuối kỳ",
                "Tiền gốc": format_money(principal),
                "Tiền lãi kỳ này": format_money(total_interest),
                "Lãi tích lũy": format_money(total_interest),
                "Tổng tiền": format_money(final_amount)
            })

    # ==============================
    # LÃI KÉP
    # ==============================
    else:

        data = []

        if payment_type == "Lãnh lãi hàng tháng":

            current_amount = principal

            monthly_rate = annual_rate / 12

            for i in range(1, months + 1):

                interest_this_period = current_amount * monthly_rate

                current_amount += interest_this_period

                data.append({
                    "Kỳ": f"Tháng {i}",
                    "Tiền gốc đầu kỳ": format_money(
                        current_amount - interest_this_period
                    ),
                    "Tiền lãi kỳ này": format_money(
                        interest_this_period
                    ),
                    "Lãi tích lũy": format_money(
                        current_amount - principal
                    ),
                    "Tổng tiền": format_money(current_amount)
                })

            final_amount = current_amount
            total_interest = final_amount - principal

        elif payment_type == "Lãnh lãi hàng quý":

            current_amount = principal
            remaining_months = months
            quarter = 0

            while remaining_months > 0:

                quarter += 1

                current_months = min(3, remaining_months)

                # Lãi kép theo số tháng thực tế
                period_rate = (
                    (1 + annual_rate / 12) ** current_months
                    - 1
                )

                interest_this_period = (
                    current_amount * period_rate
                )

                current_amount += interest_this_period

                data.append({
                    "Kỳ": f"Quý {quarter}",
                    "Tiền gốc đầu kỳ": format_money(
                        current_amount - interest_this_period
                    ),
                    "Tiền lãi kỳ này": format_money(
                        interest_this_period
                    ),
                    "Lãi tích lũy": format_money(
                        current_amount - principal
                    ),
                    "Tổng tiền": format_money(current_amount)
                })

                remaining_months -= current_months

            final_amount = current_amount
            total_interest = final_amount - principal

        else:

            # Lãi kép cuối kỳ
            monthly_rate = annual_rate / 12

            final_amount = (
                principal
                * (1 + monthly_rate) ** months
            )

            total_interest = final_amount - principal

            data.append({
                "Kỳ": "Cuối kỳ",
                "Tiền gốc đầu kỳ": format_money(principal),
                "Tiền lãi kỳ này": format_money(total_interest),
                "Lãi tích lũy": format_money(total_interest),
                "Tổng tiền": format_money(final_amount)
            })


    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.markdown("---")
    st.subheader("📊 Kết quả tính toán")

    # Lãi định kỳ
    if payment_type == "Lãnh lãi hàng tháng":

        periodic_interest = (
            data[0]["Tiền lãi kỳ này"]
            if data
            else "0 VNĐ"
        )

    elif payment_type == "Lãnh lãi hàng quý":

        periodic_interest = (
            "Xem chi tiết theo từng quý"
        )

    else:

        periodic_interest = format_money(total_interest)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💵 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {periodic_interest}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">📈 Tổng tiền lãi</div>
                <div class="result-value">
                    {format_money(total_interest)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💰 Tổng gốc + lãi</div>
                <div class="result-value">
                    {format_money(final_amount)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ==============================
    # THÔNG TIN KHOẢN GỬI
    # ==============================
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Số tiền gửi",
            format_money(principal)
        )

    with col2:
        st.metric(
            "Kỳ hạn",
            f"{months} tháng"
        )

    with col3:
        st.metric(
            "Lãi suất",
            f"{interest_rate:.2f}%/năm"
        )

    with col4:
        st.metric(
            "Hình thức",
            interest_type
        )


    # ==============================
    # BẢNG CHI TIẾT
    # ==============================
    st.markdown("---")
    st.subheader("📋 Chi tiết tiền lãi theo từng kỳ")

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ==============================
    # CÔNG THỨC
    # ==============================
    st.markdown("---")
    st.subheader("📐 Công thức tính")

    if interest_type == "Lãi đơn":

        st.markdown(
            """
            <div class="formula">

            <b>Lãi đơn:</b>

            Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12

            <br><br>

            <b>Tổng tiền nhận được:</b>

            Tổng tiền = Tiền gốc + Tiền lãi

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="formula">

            <b>Lãi kép:</b>

            Tổng tiền = Tiền gốc × (1 + Lãi suất tháng)<sup>Số tháng</sup>

            <br><br>

            Trong đó:

            <br>

            Lãi suất tháng = Lãi suất năm / 12

            <br><br>

            <b>Tổng tiền lãi:</b>

            Tổng tiền lãi = Tổng tiền − Tiền gốc

            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================
# CHÂN TRANG
# ==============================
st.markdown("---")

st.caption(
    "💡 Công cụ mang tính chất tham khảo và sử dụng công thức tính lãi suất "
    "đơn/kép theo thông tin người dùng nhập."
)
