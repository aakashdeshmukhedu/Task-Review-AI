import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Task Insight", layout="wide")

st.title("🤖 Task Review AI")
st.caption("Super Admin Dashboard Feature") 
st.markdown("⚠️ This system is for **process improvement**, not blame.")

# --------------------------------------------------
# TASK DATA (INTERNAL FACTORS INCLUDED)
# --------------------------------------------------
tasks = {
    "Sell 100 Fertilizer Boxes (Sales)": {
        "type": "Sales",
        "target": 100,
        "achieved": 88,
        "team": pd.DataFrame([
            {"Role": "Admin", "Name": "Sales Head", "Late Days": 1, "Updates": 3, "Workload": "Medium", "Done": 90, "Quality": 4.5},
            {"Role": "Senior", "Name": "Senior A", "Late Days": 0, "Updates": 4, "Workload": "Medium", "Done": 95, "Quality": 4.7},
            {"Role": "Senior", "Name": "Senior B", "Late Days": 2, "Updates": 2, "Workload": "High", "Done": 80, "Quality": 3.8},
            {"Role": "Junior", "Name": "Junior A", "Late Days": 1, "Updates": 3, "Workload": "High", "Done": 85, "Quality": 4.0},
            {"Role": "Junior", "Name": "Junior B", "Late Days": 0, "Updates": 4, "Workload": "Medium", "Done": 92, "Quality": 4.6},
            {"Role": "Junior", "Name": "Junior C", "Late Days": 3, "Updates": 1, "Workload": "High", "Done": 65, "Quality": 3.2},
        ])
    },

    "Hire Warehouse Staff (HR)": {
        "type": "HR",
        "target": None,
        "achieved": None,
        "team": pd.DataFrame([
            {"Role": "Admin", "Name": "HR Head", "Late Days": 0, "Updates": 3, "Workload": "Low", "Done": 95, "Quality": 4.6},
            {"Role": "Senior", "Name": "Senior HR 1", "Late Days": 2, "Updates": 2, "Workload": "High", "Done": 75, "Quality": 3.9},
            {"Role": "Senior", "Name": "Senior HR 2", "Late Days": 1, "Updates": 3, "Workload": "Medium", "Done": 85, "Quality": 4.2},
            {"Role": "Junior", "Name": "HR Exec A", "Late Days": 3, "Updates": 1, "Workload": "High", "Done": 60, "Quality": 3.4},
            {"Role": "Junior", "Name": "HR Exec B", "Late Days": 1, "Updates": 2, "Workload": "Medium", "Done": 80, "Quality": 4.0},
        ])
    },

    "Website Price Negotiation Feature (IT)": {
        "type": "IT",
        "target": None,
        "achieved": None,
        "team": pd.DataFrame([
            {"Role": "Admin", "Name": "IT Head", "Late Days": 0, "Updates": 4, "Workload": "Medium", "Done": 100, "Quality": 4.8},
            {"Role": "Senior", "Name": "Backend Lead", "Late Days": 3, "Updates": 2, "Workload": "High", "Done": 70, "Quality": 3.6},
            {"Role": "Senior", "Name": "Frontend Lead", "Late Days": 0, "Updates": 3, "Workload": "Medium", "Done": 90, "Quality": 4.5},
            {"Role": "Junior", "Name": "Developer A", "Late Days": 1, "Updates": 3, "Workload": "Medium", "Done": 85, "Quality": 4.2},
            {"Role": "Junior", "Name": "Developer B", "Late Days": 2, "Updates": 2, "Workload": "High", "Done": 75, "Quality": 3.8},
        ])
    },

    "Onboard 10 B2B Clients in Akola (Lead Gen)": {
        "type": "LeadGen",
        "target": 10,
        "achieved": 6,
        "team": pd.DataFrame([
            {"Role": "Admin", "Name": "Lead Gen Head", "Late Days": 0, "Updates": 3, "Workload": "Medium", "Done": 90, "Quality": 4.5},
            {"Role": "Senior", "Name": "Regional Manager", "Late Days": 2, "Updates": 2, "Workload": "High", "Done": 70, "Quality": 3.7},
            {"Role": "Senior", "Name": "Marketing Lead", "Late Days": 1, "Updates": 3, "Workload": "Medium", "Done": 80, "Quality": 4.0},
            {"Role": "Junior", "Name": "Field Exec A", "Late Days": 3, "Updates": 1, "Workload": "High", "Done": 60, "Quality": 3.3},
            {"Role": "Junior", "Name": "Field Exec B", "Late Days": 1, "Updates": 2, "Workload": "Medium", "Done": 85, "Quality": 4.1},
        ])
    }
}

# --------------------------------------------------
# TASK SELECTION
# --------------------------------------------------
task_name = st.selectbox("📌 Select Company Task", list(tasks.keys()))
task = tasks[task_name]
df = task["team"]

# SHOW CLEAN TEAM TABLE
display_df = df[["Role", "Name", "Late Days", "Updates", "Workload"]]

with st.expander("👥 Team Working on this Task"):
    st.dataframe(display_df, use_container_width=True)

# --------------------------------------------------
# AI ANALYSIS
# --------------------------------------------------
if st.button("🧠 Run AI Analysis"):

    avg_delay = df["Late Days"].mean()
    avg_done = df["Done"].mean()
    low_updates = (df["Updates"] <= 1).sum()
    overloaded = (df["Workload"] == "High").sum()

    # PERFORMANCE CLASSIFICATION
    best = df[(df["Late Days"] <= 1) & (df["Done"] >= 90) & (df["Quality"] >= 4.5)]
    good = df[(df["Late Days"] <= 2) & (df["Done"] >= 80) & (df["Quality"] >= 4.0)]
    poor = df[(df["Late Days"] >= 3) | (df["Done"] < 70)]

    st.markdown("## 📊 Executive Summary")

    if task["type"] in ["Sales", "LeadGen"]:
        st.info(f"""
        Target performance is **not fully achieved**.
        Result is **{task['achieved']} out of {task['target']}**.

        Delays and uneven workload reduced conversion efficiency.
        """)
    elif task["type"] == "HR":
        st.info("""
        Hiring progress is **slower than expected** due to overload
        and delayed candidate processing.
        """)
    else:
        st.info("""
        Feature delivery is **at risk** due to backend delays
        affecting testing and rollout.
        """)

    st.markdown("## ⭐ Team Contribution Overview")

    if not best.empty:
        st.success("**Worked Very Well**")
        for n in best["Name"]:
            st.write(f"- {n}: Timely delivery, strong output, good communication")

    if not good.empty:
        st.info("**Worked Acceptably**")
        for n in good["Name"]:
            st.write(f"- {n}: Minor delays but overall reliable contribution")

    if not poor.empty:
        st.warning("**Needs Attention (Process Support Required)**")
        for n in poor["Name"]:
            st.write(f"- {n}: Delays or overload affected task progress")

    st.markdown("## 🔍 What AI Observed (Simple Facts)")
    st.write(f"""
    - Average delay: **{avg_delay:.1f} days**
    - Actual work completed (team average): **{avg_done:.0f}%**
    - People giving very few updates: **{low_updates}**
    - People overloaded with work: **{overloaded}**
    """)

    st.markdown("## 🧩 Main Reasons for Delay")
    reasons = []
    if avg_delay > 1.5:
        reasons.append("Work was completed later than planned")
    if overloaded >= 2:
        reasons.append("Too much work assigned to few people")
    if low_updates >= 2:
        reasons.append("Problems were reported late")
    if avg_done < 80:
        reasons.append("Progress was slower than expected")

    for r in reasons:
        st.write(f"- {r}")

    st.markdown("## 🚀 AI Suggestions for Next Time")

    suggestions = {
        "Sales": [
            "Balance field workload evenly",
            "Weekly mandatory progress update",
            "Early alert if follow-up is delayed"
        ],
        "HR": [
            "Parallel interview scheduling",
            "Reduce overload on junior HR staff",
            "Weekly hiring target review"
        ],
        "IT": [
            "Break features into smaller deliveries",
            "Start testing earlier",
            "Mid-week progress review"
        ],
        "LeadGen": [
            "Improve field visit planning",
            "Early escalation for delays",
            "Balance region-wise workload"
        ]
    }

    for s in suggestions[task["type"]]:
        st.write(f"- {s}")

    st.caption("🛡️ AI insights are for management improvement, not individual blame.")
