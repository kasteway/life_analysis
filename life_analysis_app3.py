import streamlit as st
import matplotlib.pyplot as plt

# Adjusted default values (exactly 24 hours/day)
DEFAULTS = {
    "lifespan": 77,
    "sleep": 8.5,
    "work": 7.5,
    "commute": 0.5,
    "chores": 1.5,
    "meals": 1.5,
    "leisure": 2.0,
    "free_self": 1.0,
    "care_others": 0.25,
    "education": 0.25,
    "religion": 0.25,
    "shopping": 0.25,
    "misc": 0.25,
}

# Title
st.title("How Are You Spending Your Life?")

# Introduction
st.markdown("""
Welcome! This app helps you visualize how you spend your time over your expected lifespan. 
Use the sliders or dropdowns to adjust the default values and reflect on how much time you truly have for the things you enjoy most.
""")

# Reset Button and Total Hours at the Top
reset_col, hours_col = st.columns([1, 2])
with reset_col:
    if st.button("🔄 Reset to Defaults", help="Click to reset all inputs to default values"):
        for key in DEFAULTS:
            st.session_state[key] = DEFAULTS[key]

with hours_col:
    total_daily_hours_placeholder = st.empty()
    remaining_hours_placeholder = st.empty()

# Lifespan Input
lifespan = st.slider(
    "Expected lifespan (years):",
    min_value=50,
    max_value=100,
    value=st.session_state.get("lifespan", DEFAULTS["lifespan"]),
    step=1,
    key="lifespan",
)

# Activity categories
categories = {
    "Sleeping": "sleep",
    "Working": "work",
    "Commuting": "commute",
    "Household Chores": "chores",
    "Eating and Drinking": "meals",
    "Leisure": "leisure",
    "Free SELF Time": "free_self",
    "Caring for Others": "care_others",
    "Education": "education",
    "Religious and Civic Activities": "religion",
    "Shopping/Errands": "shopping",
    "Miscellaneous Activities": "misc",
}

# Layout with inputs arranged around the chart
top_row = st.columns([1, 2, 1])
bottom_row = st.columns([1, 2, 1])

# Inputs for activity durations
activity_inputs = {}
for i, (category, key) in enumerate(categories.items()):
    col = top_row[i % 3] if i < 6 else bottom_row[i % 3]
    with col:
        if category in ["Shopping/Errands", "Education", "Religion", "Miscellaneous Activities"]:
            # Use dropdown for small-value categories
            activity_inputs[key] = st.selectbox(
                f"{category} (hours):",
                [0, 0.25, 0.5, 0.75, 1.0],
                index=int(DEFAULTS[key] / 0.25),
                key=key,
            )
        else:
            # Use sliders for primary categories
            activity_inputs[key] = st.slider(
                f"{category} (hours):",
                min_value=0.0,
                max_value=24.0,
                value=st.session_state.get(key, DEFAULTS[key]),
                step=0.25,
                key=key,
            )

# Total daily hours logic
daily_hours = sum(activity_inputs.values())
remaining_hours = 24 - daily_hours

# Update total hours and feedback at the top
total_daily_hours_placeholder.markdown(
    f"<h6 style='text-align: right; font-size:14px;'>{daily_hours:.2f} hours/day ✅ You have {remaining_hours:.2f} hours remaining in your day.</h6>",
    unsafe_allow_html=True,
)

# Proportional Breakdown and Visualization
if daily_hours <= 24:
    total_hours = daily_hours * 365 * lifespan
    activities = {category: activity_inputs[key] for category, key in categories.items()}
    hours_per_activity = {activity: hours * 365 * lifespan for activity, hours in activities.items()}
    years_per_activity = {activity: hours / 24 / 365 for activity, hours in hours_per_activity.items()}
    proportions = {activity: (hours / total_hours) * 100 for activity, hours in hours_per_activity.items()}

    # Sort activities by percentage
    sorted_activities = sorted(proportions.items(), key=lambda x: x[1], reverse=True)
    sorted_labels = [activity for activity, _ in sorted_activities]
    sorted_percentages = [percentage for _, percentage in sorted_activities]
    sorted_years = [years_per_activity[activity] for activity, _ in sorted_activities]

    # Bar Chart
    st.header("Your Life Breakdown")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(sorted_labels[::-1], sorted_percentages[::-1], color='skyblue')  # Reverse for descending order
    ax.set_xlabel('Percentage of Time (%)')
    ax.set_title('Time Allocation Over Your Lifespan')
    for i, (percent, years) in enumerate(zip(sorted_percentages[::-1], sorted_years[::-1])):
        ax.text(percent + 0.5, i, f"{years:.1f} years", va='center', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

    # Detailed Breakdown Table
    st.subheader("Detailed Breakdown")
    breakdown_table = [
        {
            "Activity": activity,
            "Percentage": f"{proportion:.1f}%",
            "Time": f"{years:.1f} years" if years >= 1 else f"{int(years * 12)} months",
        }
        for activity, proportion, years in zip(sorted_labels, sorted_percentages, sorted_years)
    ]
    st.table(breakdown_table)

    # Free Time Insights
    free_years = remaining_hours * 365 * lifespan / 24 / 365
    st.subheader("Free Time Left")
    st.markdown(f"### You have approximately **{free_years:.1f} years** of free time over your lifespan.")
    st.markdown("""
    - How do you want to spend this precious free time?
    - Are there activities you can reduce to gain more time for the things you love?
    """)

    # Insights and Suggestions
    st.header("Insights and Suggestions")
    st.markdown("""
    - **Reflect**: Are you spending enough time on activities that truly matter to you?
    - **Adjust**: To gain more free time, consider minimizing:
      - Commute: Can you work remotely or move closer to work?
      - Chores: Can you delegate tasks or invest in tools to save time?
    - **Act**: Use your free time to prioritize things that bring you joy, growth, and fulfillment.
    """)

# Footer with default values source
st.markdown("""
---
**Source of Default Values:** The default values are based on the [American Time Use Survey (ATUS)](https://www.bls.gov/tus/). These reflect national averages for how people allocate time daily. For more information, visit [ATUS](https://www.bls.gov/tus/).
""")
