import streamlit as st
import uuid
import assets.edu_calc as ec
import pandas as pd
from datetime import date, datetime, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar
cal = USFederalHolidayCalendar()


# -----------------------------------------------------------
# PAGE CONFIGURATION
st.set_page_config(page_title="School Days Calculator",
                   page_icon="📅",
                   menu_items={
                       'Get help': "mailto:cgdesigned@gmail.com",
                       'About': "School Days Calculator is a tool which allows parents home schooling their children "
                                "to forecast the school year and plan out trips and days off while being able to see "
                                "the forecasted last day of school."
                   }
                   )


# CUSTOM STYLES
st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>',
         unsafe_allow_html=True)

# VARIABLES
today = datetime.now()
tomorrow = datetime.now() + timedelta(days=1)
next_year = today.year + 1
jan_1 = date(next_year, 1, 1)
dec_31 = date(next_year, 12, 31)

# -----------------------------------------------------------
# SIDEBAR
st.sidebar.markdown("# School Year Details:")
d = st.sidebar.date_input('School Start Date', value=None, format="MM/DD/YYYY")
if d is not None:
    start_date = datetime(d.year, d.month, d.day)
n_days = st.sidebar.number_input('Number of School Days', value=None, min_value=1, max_value=365, step=1)


# -----------------------------------------------------------
# Content

if "rows" not in st.session_state:
    st.session_state["rows"] = []

rows_collection = []


def add_row():
    element_id = uuid.uuid4()
    st.session_state["rows"].append(str(element_id))


def remove_row(row_id):
    st.session_state["rows"].remove(str(row_id))


def generate_row(row_id):
    row_container = st.empty()
    row_columns = row_container.columns((3, 2, 1))
    row_name = row_columns[0].text_input("Description", key=f"txt_{row_id}")
    row_date_range = row_columns[1].date_input("Select your days off",
                                               (today, tomorrow), format="MM/DD/YYYY", key=f"dt_{row_id}")
    if len(row_date_range) != 2:
        st.stop()
    row_date_range = (row_date_range[0].strftime("%Y-%m-%d"), row_date_range[1].strftime("%Y-%m-%d"))
    row_columns[2].button("🗑️", key=f"del_{row_id}", on_click=remove_row, args=[row_id])
    return {"description": row_name, "dates": row_date_range}


st.markdown("""# <i class="fa-solid fa-calculator"></i>  School Days Calculator""", unsafe_allow_html=True)
st.markdown("""Descriptive text and instructions can go here...""")
st.markdown("#### Track Days Off.")

for row in st.session_state["rows"]:
    row_data = generate_row(row)
    rows_collection.append(row_data)

menu = st.columns(2)
trips = []

with menu[0]:
    st.button("Add Record", on_click=add_row)
if len(rows_collection) > 0:
    st.subheader("Collected Data")
    display = st.columns(2)
    data = pd.DataFrame(rows_collection)
    data.rename(columns={"description": "Description", "dates": "Days Off"}, inplace=True)
    display[0].dataframe(data=data, use_container_width=True)
    # display[1].bar_chart(data=data, x="Item Name", y="Quantity")
    trips = data['Days Off'].to_list()

if d is not None and n_days is not None:
    last_day = ec.calc_end_date(start_date, n_days, cal, trips)
    with st.sidebar:
        st.title("Projected Last Day of School:")
        st.success(f"{last_day.strftime('%A, %B %d, %Y')}")
