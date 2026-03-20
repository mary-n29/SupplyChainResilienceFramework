"""
Supply Chain Resilience Framework Dashboard
Tab 1: Metric Scoring by Stage / Capability
Tab 2: Metric Definitions Reference
"""

import sys, os

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

import dash
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# ============================================================================
# DATA
# ============================================================================

stages = ["Prepare", "Prevent", "Absorb", "Recover", "Adapt"]

capabilities = [
    "Anticipation", "Risk Management Culture", "Knowledge Management",
    "Visibility", "Security", "Efficiency", "Market Position", "Redundancy",
    "Financial Strength", "Flexibility in Sourcing and Capacity",
    "HR Management", "Organization", "Innovation", "Agility"
]

# ●●● = 3, ●● = 2, ● = 1, ○ = 0
capability_stage_weights = {
    "Visibility":                        {"Prepare": 3, "Prevent": 3, "Absorb": 2, "Recover": 0, "Adapt": 2},
    "Efficiency":                        {"Prepare": 2, "Prevent": 3, "Absorb": 0, "Recover": 0, "Adapt": 2},
    "Agility":                           {"Prepare": 2, "Prevent": 2, "Absorb": 2, "Recover": 3, "Adapt": 2},
    "Redundancy":                        {"Prepare": 2, "Prevent": 3, "Absorb": 2, "Recover": 0, "Adapt": 0},
    "Anticipation":                      {"Prepare": 3, "Prevent": 2, "Absorb": 0, "Recover": 0, "Adapt": 0},
    "Organization":                      {"Prepare": 0, "Prevent": 0, "Absorb": 3, "Recover": 3, "Adapt": 2},
    "Risk Management Culture":           {"Prepare": 3, "Prevent": 2, "Absorb": 2, "Recover": 0, "Adapt": 0},
    "Knowledge Management":              {"Prepare": 2, "Prevent": 2, "Absorb": 2, "Recover": 2, "Adapt": 3},
    "Financial Strength":                {"Prepare": 0, "Prevent": 0, "Absorb": 3, "Recover": 2, "Adapt": 0},
    "Security":                          {"Prepare": 2, "Prevent": 3, "Absorb": 0, "Recover": 0, "Adapt": 0},
    "Market Position":                   {"Prepare": 0, "Prevent": 0, "Absorb": 3, "Recover": 2, "Adapt": 0},
    "HR Management":                     {"Prepare": 0, "Prevent": 0, "Absorb": 2, "Recover": 3, "Adapt": 2},
    "Innovation":                        {"Prepare": 0, "Prevent": 0, "Absorb": 0, "Recover": 2, "Adapt": 3},
    "Flexibility in Sourcing and Capacity": {"Prepare": 2, "Prevent": 2, "Absorb": 3, "Recover": 2, "Adapt": 2},
}

metrics_data = [
    # --- Operational Resilience ---
    {"name": "Inventory location accuracy rate",       "primary_stage": "Prepare",                          "category": "Operational"},
    {"name": "Real-time tracking coverage",            "primary_stage": "Prepare",                                         "category": "Operational"},
    {"name": "Supply chain event detection rate",      "primary_stage": "Prepare",                        "category": "Operational"},
    {"name": "Stock availability rate",                "primary_stage": "Absorb",                                 "category": "Operational"},
    {"name": "Supplier defect rate",                   "primary_stage": "Prevent",             "category": "Operational"},
    {"name": "Customer wait time for org maintenance", "primary_stage": "Recover",                                    "category": "Operational"},
    {"name": "On-time definitive delivery compliance", "primary_stage": "Absorb",                                                     "category": "Operational"},
    {"name": "Not mission capable supply backorders",  "primary_stage": "Absorb",                                       "category": "Operational"},
    {"name": "Wholesale supply availability",          "primary_stage": "Absorb",                                    "category": "Operational"},
    {"name": "Procurement lead variance",              "primary_stage": "Prevent",                                   "category": "Operational"},
    # --- Structural Resilience ---
    {"name": "Network concentration risk",             "primary_stage": "Prevent",                    "category": "Structural"},
    {"name": "Alternate source coverage",              "primary_stage": "Prevent",  "category": "Structural"},
    {"name": "Multi-path logistics coverage",          "primary_stage": "Prevent",                                      "category": "Structural"},
    {"name": "Supplier financial risk score",          "primary_stage": "Prevent",      "category": "Structural"},
    {"name": "Design lock-in severity",                "primary_stage": "Prevent",  "category": "Structural"},
    {"name": "Critical skill and capability coverage", "primary_stage": "Prepare",               "category": "Structural"},
    {"name": "Demand volatility",                      "primary_stage": "Prepare",                "category": "Structural"},
    # --- Functional Resilience ---
    {"name": "Demand forecast accuracy",               "primary_stage": "Prevent",                                        "category": "Functional"},
    {"name": "Procurement cycle time",                 "primary_stage": "Prevent",                               "category": "Functional"},
    {"name": "Time-to-survive",                        "primary_stage": "Absorb",                "category": "Functional"},
    {"name": "Time-to-recover",                        "primary_stage": "Recover",                                  "category": "Functional"},
    {"name": "Recovery effectiveness rate",            "primary_stage": "Recover",                    "category": "Functional"},
    {"name": "Time-to-recover improvement",            "primary_stage": "Adapt",        "category": "Functional"},
]

# ============================================================================
# METRICS REFERENCE DATA (for Tab 2)
# ============================================================================

metrics_reference = {
    "Inventory location accuracy rate": {
        "category": "Operational Resilience",
        "definition": "The percentage of inventory items correctly recorded in the system as being in the right physical location.",
        "justification": "Poor location accuracy leads to delays, stockouts, and wasted labor especially during disruptions when speed matters most. High accuracy supports faster response and recovery.",
      #  "capabilities": "Visibility, Efficiency, Knowledge Management",
        "stages": "Prepare, Prevent, Adapt",
        "update_frequency": "Weekly or monthly",
    },
    "Real-time tracking coverage": {
        "category": "Operational Resilience",
        "definition": "The percentage of shipments or assets that can be tracked in real time throughout the supply chain network.",
        "justification": "Real-time visibility improves disruption detection, response speed, and rerouting capability. It enables proactive intervention rather than reactive response.",
       # "capabilities": "Visibility, Agility, Security",
        "stages": "Prepare, Prevent",
        "update_frequency": "Monthly",
    },
    "Supply chain event detection rate": {
        "category": "Operational Resilience",
        "definition": "The percentage of disruption events such as delays, shortages, supplier failures detected early enough to allow corrective action before service failure occurs.",
        "justification": "Early detection is critical to resilience. Higher detection rates indicate strong monitoring and intelligence capabilities that enable proactive mitigation.",
     #   "capabilities": "Anticipation, Visibility, Knowledge Management",
        "stages": "Prevent, Absorb, Recover",
        "update_frequency": "Weekly or monthly",
    },
    "Stock availability rate": {
        "category": "Operational Resilience",
        "definition": "The percentage of time critical stock items are available to meet demand without backorders.",
        "justification": "Stock availability is a fundamental resilience indicator. High availability ensures continuity during disruptions and reduces operational downtime.",
      #  "capabilities": "Redundancy, Efficiency, Visibility",
        "stages": "Absorb",
        "update_frequency": "Weekly or monthly",
    },
    "Supplier defect rate": {
        "category": "Operational Resilience",
        "definition": "The percentage of supplier delivered units that fail quality inspection or result in returns or refunds.",
        "justification": "High defect rates increase downtime, reduce usable inventory, and slow recovery during disruptions. Supplier quality reliability is essential for resilient supply chains.",
      #  "capabilities": "Efficiency, Risk Management Culture, Knowledge Management",
        "stages": "Prevent, Absorb",
        "update_frequency": "Monthly",
    },
    "Customer wait time for org maintenance": {
        "category": "Operational Resilience",
        "definition": "The average time customers wait for scheduled or corrective organizational-level maintenance services due to part or labor constraints.",
        "justification": "Long wait times reflect poor maintenance supply readiness and weak repair pipeline resilience. Reducing delays improves service reliability and recovery performance.",
       # "capabilities": "Efficiency, Visibility, Redundancy",
        "stages": "Recover",
        "update_frequency": "Monthly",
    },
    "On-time definitive delivery compliance": {
        "category": "Operational Resilience",
        "definition": "The percentage of orders delivered on or before the committed delivery date, measuring the reliability of the supply chain in meeting customer commitments.",
        "justification": "On-time delivery is a fundamental measure of supply chain performance and reliability. Maintaining high on-time delivery rates demonstrates the supply chain's ability to absorb shocks and recover quickly.",
       # "capabilities": "Efficiency, Agility",
        "stages": "Prepare, Prevent",
        "update_frequency": "Weekly or monthly",
    },
    "Not mission capable supply backorders": {
        "category": "Operational Resilience",
        "definition": "The number or percentage of supply related backorders preventing assets/equipment from being mission capable due to missing parts/materials.",
        "justification": "Backorders that directly reduce mission capability are a strong indicator of fragility in supply chain and lack of sufficient buffers. Reducing this improves readiness and resilience.",
      #  "capabilities": "Efficiency, Agility, Visibility",
        "stages": "Prepare, Prevent, Adapt",
        "update_frequency": "Weekly or monthly",
    },
    "Wholesale supply availability": {
        "category": "Operational Resilience",
        "definition": "The percentage of requested wholesale inventory fulfilled immediately from available stock without delay.",
        "justification": "High wholesale availability signals strong inventory positioning and fulfillment capability. Low availability indicates vulnerability to demand spikes or upstream disruptions.",
      #  "capabilities": "Efficiency, Visibility, Redundancy",
        "stages": "Prepare, Prevent",
        "update_frequency": "Weekly or monthly",
    },
    "Procurement lead variance": {
        "category": "Operational Resilience",
        "definition": "The variability or standard deviation in procurement lead times, measuring the consistency and reliability of supplier delivery schedules.",
        "justification": "High lead time variance indicates supply chain instability and unpredictability, which reduces resilience by making it difficult to plan inventory levels and production schedules.",
      #  "capabilities": "Anticipation, Organization, Agility",
        "stages": "Prepare, Prevent",
        "update_frequency": "Monthly",
    },
    "Network concentration risk": {
        "category": "Structural Resilience",
        "definition": "A measure of dependency on a limited number of suppliers, facilities, transportation lanes, or geographic regions for critical supply chain flows.",
        "justification": "Highly concentrated supply networks are more vulnerable to single points of failure. Diversification reduces the impact of disruptions and improves resilience against regional or supplier-specific shocks.",
      #  "capabilities": "Risk Management Culture, Redundancy, Anticipation",
        "stages": "Prepare, Prevent, Absorb",
        "update_frequency": "Quarterly",
    },
    "Alternate source coverage": {
        "category": "Structural Resilience",
        "definition": "The percentage of critical items or components that have qualified alternate suppliers or substitute sources.",
        "justification": "Alternate sourcing improves resilience by enabling fast switching when primary suppliers fail. Higher coverage reduces dependency and strengthens continuity planning.",
      #  "capabilities": "Flexibility in Sourcing and Capacity, Redundancy, Market Position",
        "stages": "Prepare, Prevent, Absorb",
        "update_frequency": "Quarterly",
    },
    "Multi-path logistics coverage": {
        "category": "Structural Resilience",
        "definition": "The percentage of shipments or critical supply routes supported by multiple feasible transportation paths or modes such as air, sea, rail, or ground.",
        "justification": "Multi-path logistics reduces disruption risks caused by lane closures, port congestion, or carrier failures. Greater route flexibility improves supply chain continuity.",
       # "capabilities": "Redundancy, Agility, Visibility",
        "stages": "Prepare, Prevent, Absorb",
        "update_frequency": "Quarterly",
    },
    "Supplier financial risk score": {
        "category": "Structural Resilience",
        "definition": "A composite risk rating assessing supplier financial stability based on liquidity, credit rating, debt, profitability, and bankruptcy likelihood.",
        "justification": "Financially unstable suppliers are more likely to fail during disruptions, leading to sudden supply interruptions. Monitoring this reduces the risk of surprise collapses.",
       # "capabilities": "Financial Strength, Risk Management Culture, Anticipation",
        "stages": "Prepare, Prevent",
        "update_frequency": "Quarterly or semi-annually",
    },
    "Design lock-in severity": {
        "category": "Structural Resilience",
        "definition": "A measure of how difficult it is to substitute parts or suppliers due to proprietary specifications, certifications, or unique engineering requirements.",
        "justification": "Highly locked-in designs reduce sourcing flexibility and slow recovery during shortages. Lower lock-in increases adaptability and improves resilience under supplier disruptions.",
       # "capabilities": "Innovation, Flexibility in Sourcing and Capacity, Risk Management Culture",
        "stages": "Prepare, Prevent, Absorb",
        "update_frequency": "Semi-annually or annually",
    },
    "Critical skill and capability coverage": {
        "category": "Structural Resilience",
        "definition": "The percentage of required critical roles/skills that are staffed, trained, and available to support the supply chain's operations.",
        "justification": "Resilience depends heavily on people and expertise. Gaps in critical skills reduce the ability to respond and adapt to disruptions, as well as execute recovery plans effectively.",
      #  "capabilities": "HR Management, Knowledge Management, Organization",
        "stages": "Prepare, Prevent, Absorb",
        "update_frequency": "Quarterly",
    },
    "Demand volatility": {
        "category": "Structural Resilience",
        "definition": "A statistical measure of demand variability over time, which often uses a standard deviation or coefficient of variance.",
        "justification": "High demand volatility increases forecasting difficulty and inventory risk. Measuring volatility helps organizations prepare buffers and adaptive planning mechanisms.",
       # "capabilities": "Anticipation, Knowledge Management, Visibility",
        "stages": "Prepare, Prevent, Absorb, Recover, Adapt",
        "update_frequency": "Monthly or quarterly",
    },
    "Demand forecast accuracy": {
        "category": "Functional Resilience",
        "definition": "The degree to which forecasted demand aligns with actual demand over a specified time period, measuring the precision of demand prediction models.",
        "justification": "Accurate demand forecasting is fundamental to anticipatory resilience. Organizations with superior forecasting can proactively position inventory and capacity to absorb disruptions without service failures.",
      #  "capabilities": "Anticipation, Organization",
        "stages": "Prepare, Prevent",
        "update_frequency": "Monthly or quarterly",
    },
    "Procurement cycle time": {
        "category": "Functional Resilience",
        "definition": "The average time required to complete the procurement process from requisition initiation to purchase order placement.",
        "justification": "Long procurement cycles reduce responsiveness and increase exposure during disruptions. Shorter cycle times increase agility and enable faster sourcing adjustments.",
    #    "capabilities": "Efficiency, Agility, Organization",
        "stages": "Prepare, Prevent, Adapt",
        "update_frequency": "Monthly",
    },
    "Time-to-survive": {
        "category": "Functional Resilience",
        "definition": "The maximum duration the supply chain can continue meeting demand after a disruption before service failure occurs without replenishment.",
        "justification": "Time-to-survive quantifies resilience buffers such as inventory, capacity, and flexibility. A longer time-to-survive gives organizations more time to respond and avoid operational collapse.",
      #  "capabilities": "Redundancy, Risk Management Culture, Anticipation",
        "stages": "Recover",
        "update_frequency": "Quarterly",
    },
    "Time-to-recover": {
        "category": "Functional Resilience",
        "definition": "The time required for the supply chain to return to normal performance levels after a disruption event.",
        "justification": "Time-to-recover is one of the clearest indicators of resilience maturity. Shorter recovery times demonstrate strong contingency planning, agility, and response execution.",
       # "capabilities": "Agility, Organization, Redundancy",
        "stages": "Recover, Adapt",
        "update_frequency": "After disruptions",
    },
    "Recovery effectiveness rate": {
        "category": "Functional Resilience",
        "definition": "The percentage of disruption events that are resolved successfully within defined recovery targets such as time, cost, or service level.",
        "justification": "This metric measures resilience effectiveness in practice, not just planning. Higher ratios indicate strong crisis response, coordination, and recovery execution.",
     #   "capabilities": "Risk Management Culture, Organization, Agility",
        "stages": "Recover",
        "update_frequency": "Quarterly",
    },
    "Time-to-recover improvement": {
        "category": "Functional Resilience",
        "definition": "The percentage reduction in time-to-recover (TTR) across comparable disruption events over time, measuring the extent to which recovery performance improves through learning and adaptation.",
        "justification": "Improvements in recovery time reflect the supply chain's ability to learn from disruptions and enhance response effectiveness. Faster recovery across events indicates increased adaptability and the successful application of lessons learned.",
     #   "capabilities": "Knowledge Management, Agility, Organization, Innovation",
        "stages": "Adapt",
        "update_frequency": "After disruptions",
    },
}

category_descriptions = {
    "Operational Resilience": {
        "subtitle": "Resilience today",
        "description": "Day-to-day performance metrics reflecting how well the supply chain executes core activities under normal and mildly disrupted conditions.",
        "color": "#f0f4f8",       # cool light slate
        "border": "#4a6fa5",      # steel blue
        "text": "#2d4a6e",
        "badge_bg": "#4a6fa5",
    },
    "Structural Resilience": {
        "subtitle": "Fragility by design",
        "description": "Network architecture and configuration metrics revealing whether the supply chain is built for durability or carries inherent structural vulnerabilities.",
        "color": "#f0f5f2",       # soft sage
        "border": "#3d7a5e",      # deep teal-green
        "text": "#264d3b",
        "badge_bg": "#3d7a5e",
    },
    "Functional Resilience": {
        "subtitle": "Dynamic response & recovery",
        "description": "Metrics capturing how effectively the supply chain responds and recovers when disruptions occur — forecasting, speed, survival time, and recovery rate.",
        "color": "#f5f2f0",       # warm light stone
        "border": "#7a5c3d",      # warm brown-slate
        "text": "#4d3626",
        "badge_bg": "#7a5c3d",
    },
}

# ============================================================================
# SCORING LOGIC
# ============================================================================

def score_metrics(selected_stage=None, selected_capability=None):
    results = []
    for m in metrics_data:
        stage_score = None
        cap_score = None

        if selected_stage:
            s = 0
            if m["primary_stage"] == selected_stage:
                s += 3
            for cap in m["capabilities"]:
                s += capability_stage_weights.get(cap, {}).get(selected_stage, 0)
            stage_score = s

        if selected_capability:
            c = 0
            if selected_capability in m["capabilities"]:
                c += 3
                c += capability_stage_weights.get(selected_capability, {}).get(m["primary_stage"], 0)
            cap_score = c

        if stage_score is not None and cap_score is not None:
            final_score = (stage_score + cap_score) / 2
        elif stage_score is not None:
            final_score = stage_score
        elif cap_score is not None:
            final_score = cap_score
        else:
            final_score = None

        results.append({
            "name": m["name"],
            "score": final_score,
            "category": m["category"],
            "primary_stage": m["primary_stage"],
            "capabilities": m["capabilities"],
        })

    return results


def group_by_category(scored):
    grouped = {"Operational": [], "Structural": [], "Functional": []}
    for item in scored:
        grouped[item["category"]].append(item)
    for cat in grouped:
        grouped[cat].sort(key=lambda x: (x["score"] or 0), reverse=True)
    return grouped


# ============================================================================
# LAYOUT HELPERS
# ============================================================================

def make_metric_card(item, show_score, max_score=12):
    cat = item["category"] + " Resilience"
    cat_info = category_descriptions[cat]
    score = item["score"]

    score_badge = html.Span()
    card_opacity = 1.0
    if show_score and score is not None:
        # Map score to 1-5 stars relative to max_score
        if max_score > 0:
            ratio = score / max_score
        else:
            ratio = 0
        stars = max(1, round(ratio * 5)) if score > 0 else 1
        filled = "★" * stars
        empty  = "☆" * (5 - stars)
        card_opacity = 0.3 + 0.7 * ratio

        score_badge = html.Span(
            [
                html.Span(filled, style={"color": cat_info["badge_bg"]}),
                html.Span(empty,  style={"color": "#ccc"}),
            ],
            style={
                "fontSize": "16px",
                "letterSpacing": "1px",
                "float": "right",
                "lineHeight": "1",
            }
        )

    return html.Div([
        html.Div([
            html.Span(item["name"], style={"fontSize": "13px", "fontWeight": "500", "flex": "1", "paddingRight": "8px"}),
            score_badge,
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "space-between"}),
        html.Div(
            f"Primary: {item['primary_stage']}",
            style={"fontSize": "11px", "color": "#888", "marginTop": "3px"}
        ),
    ], style={
        "backgroundColor": "white",
        "border": f"1px solid {cat_info['border']}33",
        "borderRadius": "6px",
        "padding": "10px 12px",
        "marginBottom": "6px",
        "opacity": str(card_opacity),
        "transition": "opacity 0.3s",
    })


def make_category_column(cat_key, items, show_score, max_score=12):
    cat_name = cat_key + " Resilience"
    cat_info = category_descriptions[cat_name]

    metric_cards = [make_metric_card(item, show_score, max_score) for item in items]

    return dbc.Col([
        html.Div([
            html.Div([
                html.H5(cat_name, style={"color": cat_info["text"], "marginBottom": "2px", "fontSize": "15px"}),
                html.Div(cat_info["subtitle"], style={"fontSize": "11px", "color": "#888", "fontStyle": "italic", "marginBottom": "6px"}),
                html.P(cat_info["description"], style={"fontSize": "12px", "color": "#555", "marginBottom": "12px"}),
            ]),
            html.Div(metric_cards),
        ], style={
            "backgroundColor": cat_info["color"],
            "borderTop": f"4px solid {cat_info['border']}",
            "borderRadius": "8px",
            "padding": "16px",
            "height": "100%",
        })
    ], width=4)


# ============================================================================
# REFERENCE PAGE
# ============================================================================

def make_reference_page():
    cards = []
    for cat, cat_info in category_descriptions.items():
        cat_key = cat.replace(" Resilience", "")
        cat_metrics = [m for m, info in metrics_reference.items() if info["category"] == cat]
        metric_rows = []
        for m in cat_metrics:
            info = metrics_reference[m]
            metric_rows.append(
                html.Tr([
                    html.Td(html.Strong(m), style={"width": "20%", "verticalAlign": "top", "paddingRight": "12px", "paddingBottom": "10px"}),
                    html.Td(info["definition"], style={"width": "35%", "verticalAlign": "top", "paddingRight": "12px", "paddingBottom": "10px"}),
                    html.Td(info["justification"], style={"width": "30%", "verticalAlign": "top", "paddingRight": "12px", "paddingBottom": "10px", "color": "#555"}),
                    html.Td([
                        html.Div(["Capabilities: ", html.Em(info["capabilities"])], style={"fontSize": "12px", "color": "#666"}),
                        html.Div(["Stages: ", html.Em(info["stages"])], style={"fontSize": "12px", "color": "#666", "marginTop": "4px"}),
                        html.Div(["Frequency: ", html.Em(info["update_frequency"])], style={"fontSize": "12px", "color": "#888", "marginTop": "4px"}),
                    ], style={"width": "15%", "verticalAlign": "top", "paddingBottom": "10px"}),
                ], style={"borderBottom": "1px solid #eee"})
            )

        cards.append(
            dbc.Card([
                dbc.CardHeader([
                    html.H4(cat, className="mb-0", style={"color": cat_info.get("text", cat_info["border"])}),
                    html.Small(cat_info["subtitle"], className="text-muted ms-2"),
                ]),
                dbc.CardBody([
                    html.P(cat_info["description"], style={"fontStyle": "italic", "color": "#444", "marginBottom": "16px"}),
                    html.Table([
                        html.Thead(html.Tr([
                            html.Th("Metric", style={"width": "20%", "paddingBottom": "8px"}),
                            html.Th("Definition", style={"width": "35%", "paddingBottom": "8px"}),
                            html.Th("Why It Matters", style={"width": "30%", "paddingBottom": "8px"}),
                            html.Th("Details", style={"width": "15%", "paddingBottom": "8px"}),
                        ], style={"backgroundColor": "#f8f9fa"})),
                        html.Tbody(metric_rows),
                    ], style={"width": "100%", "borderCollapse": "collapse", "fontSize": "13px"}),
                ]),
            ], className="mb-4", style={"borderLeft": f"4px solid {cat_info['border']}"})
        )
    return cards


# ============================================================================
# APP
# ============================================================================

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def make_toggle_btn(label, btn_id, color):
    return dbc.Button(
        label,
        id=btn_id,
        outline=True,
        color=color,
        className="me-2 mb-2",
        n_clicks=0,
        style={"fontSize": "15px", "padding": "8px 20px", "borderRadius": "6px", "fontWeight": "500"},
    )

stage_buttons = html.Div([
    html.Div("Stage", style={"fontWeight": "700", "fontSize": "13px", "textTransform": "uppercase",
                              "letterSpacing": "0.05em", "color": "#666", "marginBottom": "6px"}),
    html.Div([make_toggle_btn(s, f"stage-btn-{s}", "danger") for s in stages],
             style={"display": "flex", "flexWrap": "wrap"}),
])

cap_buttons = html.Div([
    html.Div("Capability", style={"fontWeight": "700", "fontSize": "13px", "textTransform": "uppercase",
                                   "letterSpacing": "0.05em", "color": "#666", "marginBottom": "6px", "marginTop": "12px"}),
    html.Div([make_toggle_btn(c, f"cap-btn-{c.replace(' ', '-')}", "primary") for c in capabilities],
             style={"display": "flex", "flexWrap": "wrap"}),
])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Supply Chain Resilience Framework", className="text-center mb-2"),
        ], width=12)
    ]),

    dbc.Tabs([

        # ── Tab 0: About ─────────────────────────────────────────────────────
        dbc.Tab(label="ℹ️ About", tab_id="tab-about", children=[
            html.Div([
                html.H2("About This Dashboard", className="mb-3 mt-2",
                        style={"color": "#2d4a6e", "fontWeight": "700"}),
                html.P(
                    "This dashboard is designed to support data-driven decision-making for supply chain resilience. "
                    "It helps you identify which metrics matter most based on your specific resilience objective "
                    "and understand the capabilities that drive performance.",
                    style={"fontSize": "15px", "color": "#333", "marginBottom": "20px"}
                ),
                dbc.Card([
                    dbc.CardHeader(html.Strong("The framework is built around three key elements:")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div("🕐", style={"fontSize": "28px", "marginBottom": "6px"}),
                                html.Strong("Resilience Stages"),
                                html.P("When resilience is needed (e.g., Prepare, Recover, Adapt)",
                                       style={"fontSize": "13px", "color": "#555", "marginTop": "4px"}),
                            ], width=4, className="text-center"),
                            dbc.Col([
                                html.Div("⚙️", style={"fontSize": "28px", "marginBottom": "6px"}),
                                html.Strong("Capabilities"),
                                html.P("How resilience is achieved (e.g., Agility, Visibility)",
                                       style={"fontSize": "13px", "color": "#555", "marginTop": "4px"}),
                            ], width=4, className="text-center"),
                            dbc.Col([
                                html.Div("📏", style={"fontSize": "28px", "marginBottom": "6px"}),
                                html.Strong("Metrics"),
                                html.P("What is measured (e.g., Time-to-Recover, Stock Availability)",
                                       style={"fontSize": "13px", "color": "#555", "marginTop": "4px"}),
                            ], width=4, className="text-center"),
                        ]),
                        html.Hr(),
                        html.P([
                            "All analysis ultimately leads to ",
                            html.Strong("metrics"),
                            ", which provide actionable performance insights."
                        ], className="mb-0 text-center", style={"fontSize": "14px", "color": "#444"}),
                    ]),
                ], className="mb-4", style={"borderLeft": "4px solid #2d4a6e"}),

                html.H4("How to Use the Dashboard", className="mb-3",
                        style={"color": "#2d4a6e", "fontWeight": "700"}),

                dbc.Accordion([
                    dbc.AccordionItem([
                        html.P("Begin by selecting either:"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Badge("Option A", color="danger", className="mb-2"),
                                html.P([html.Strong("A Resilience Stage"), " → e.g., \"Recover\" (improve recovery performance)"],
                                       style={"fontSize": "14px"}),
                            ], width=6),
                            dbc.Col([
                                dbc.Badge("Option B", color="primary", className="mb-2"),
                                html.P([html.Strong("A Capability"), " → e.g., \"Agility\" (assess responsiveness)"],
                                       style={"fontSize": "14px"}),
                            ], width=6),
                        ]),
                        html.P("This defines your decision context.", style={"color": "#555", "marginBottom": "0"}),
                    ], title="Step 1 — Start with Your Objective"),
                    dbc.AccordionItem([
                        html.P("If a stage is selected, the dashboard highlights capabilities most important for that stage."),
                        html.Ul([
                            html.Li("Strongly related capabilities are emphasized"),
                            html.Li("Less relevant capabilities are de-emphasised"),
                        ]),
                        dbc.Alert("\"What drives performance in this area?\"",
                                  color="light", style={"fontStyle": "italic", "borderLeft": "4px solid #aaa"}),
                    ], title="Step 2 — Review Relevant Capabilities"),
                    dbc.AccordionItem([
                        html.P("The dashboard displays a ranked list of metrics based on your selection."),
                        html.Ul([
                            html.Li("Metrics are not filtered out, but prioritized"),
                            html.Li("Rankings reflect alignment with your selected stage and the contribution of underlying capabilities"),
                        ]),
                        dbc.Alert("\"What should I measure and focus on?\"",
                                  color="light", style={"fontStyle": "italic", "borderLeft": "4px solid #aaa"}),
                    ], title="Step 3 — Analyse Prioritised Metrics"),
                    dbc.AccordionItem([
                        html.P("Metric relevance is shown as a star rating (1–5):"),
                        dbc.Row([
                            dbc.Col(dbc.Badge("★★★★★  High relevance",   color="success", className="w-100 mb-2 p-2"), width=4),
                            dbc.Col(dbc.Badge("★★★☆☆  Medium relevance", color="warning", text_color="dark", className="w-100 mb-2 p-2"), width=4),
                            dbc.Col(dbc.Badge("★☆☆☆☆  Low relevance",    color="secondary", className="w-100 mb-2 p-2"), width=4),
                        ]),
                        html.P("Even if a metric is not directly tied to your selected stage, it still appears if it contributes through relevant capabilities.",
                               style={"color": "#555", "marginBottom": "0"}),
                    ], title="Step 4 — Interpret Metric Relevance"),
                    dbc.AccordionItem([
                        html.P("Metrics are grouped into three categories:"),
                        dbc.Row([
                            dbc.Col([
                                html.Div(style={"height": "4px", "backgroundColor": "#4a6fa5", "borderRadius": "2px", "marginBottom": "6px"}),
                                html.Strong("Operational"), html.Br(),
                                html.Span("Current performance", style={"fontSize": "13px", "color": "#555"}),
                            ], width=4),
                            dbc.Col([
                                html.Div(style={"height": "4px", "backgroundColor": "#3d7a5e", "borderRadius": "2px", "marginBottom": "6px"}),
                                html.Strong("Structural"), html.Br(),
                                html.Span("System design and robustness", style={"fontSize": "13px", "color": "#555"}),
                            ], width=4),
                            dbc.Col([
                                html.Div(style={"height": "4px", "backgroundColor": "#7a5c3d", "borderRadius": "2px", "marginBottom": "6px"}),
                                html.Strong("Functional"), html.Br(),
                                html.Span("Response and improvement over time", style={"fontSize": "13px", "color": "#555"}),
                            ], width=4),
                        ]),
                        html.P("These categories provide context but do not limit what is shown.",
                               style={"color": "#555", "marginBottom": "0", "marginTop": "12px"}),
                    ], title="Step 5 — Understand Metric Context"),
                ], start_collapsed=False, className="mb-4"),

                dbc.Card([
                    dbc.CardHeader(html.Strong("⚙️  How the Logic Works (Behind the Scenes)")),
                    dbc.CardBody([
                        html.P("Metric relevance is determined using a weighted approach:"),
                        html.Ul([
                            html.Li("Metrics aligned with your selected stage receive higher priority"),
                            html.Li("Additional weighting is applied based on how strongly their associated capabilities support that stage"),
                        ]),
                        html.P("This ensures that:", style={"marginBottom": "4px"}),
                        html.Ul([
                            html.Li("The most directly relevant metrics are prioritized"),
                            html.Li("Supporting metrics are still visible"),
                            html.Li("No important information is hidden"),
                        ], style={"marginBottom": "0"}),
                    ]),
                ], className="mb-4", style={"borderLeft": "4px solid #888"}),

                dbc.Card([
                    dbc.CardHeader(html.Strong("✅  What This Helps You Do")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.Div([
                                html.Div("🎯", style={"fontSize": "22px"}),
                                html.P("Identify the most relevant metrics for your resilience objective",
                                       style={"fontSize": "13px", "marginTop": "6px"}),
                            ], className="text-center"), width=4),
                            dbc.Col(html.Div([
                                html.Div("🔍", style={"fontSize": "22px"}),
                                html.P("Understand the capabilities driving performance",
                                       style={"fontSize": "13px", "marginTop": "6px"}),
                            ], className="text-center"), width=4),
                            dbc.Col(html.Div([
                                html.Div("📈", style={"fontSize": "22px"}),
                                html.P("Focus improvement efforts on measurable, high-impact areas",
                                       style={"fontSize": "13px", "marginTop": "6px"}),
                            ], className="text-center"), width=4),
                        ]),
                    ]),
                ], style={"borderLeft": "4px solid #2ecc71"}),

            ], style={"padding": "24px", "maxWidth": "900px", "margin": "0 auto"})
        ]),

        # ── Tab 1: Scoring ──────────────────────────────────────────────────
        dbc.Tab(label="📊 Metric Scoring", tab_id="tab-scoring", children=[
            html.Div([
                # Selection controls
                dbc.Card([
                    dbc.CardBody([
                        stage_buttons,
                        cap_buttons,
                        html.Div(id="selection-label", style={"marginTop": "10px", "fontSize": "13px", "color": "#555"}),
                    ])
                ], className="mb-4 mt-3"),

                # Hidden stores for current selections
                dcc.Store(id="selected-stage", data=None),
                dcc.Store(id="selected-capability", data=None),

                # Metric columns
                html.Div(id="metric-columns"),
            ], style={"padding": "0 8px"})
        ]),

        # ── Tab 2: Definitions ──────────────────────────────────────────────
        dbc.Tab(label="📋 Metric Definitions", tab_id="tab-reference", children=[
            html.Div(make_reference_page(), style={"padding": "24px"})
        ]),

    ], id="main-tabs", active_tab="tab-about"),

], fluid=True)


# ============================================================================
# CALLBACKS
# ============================================================================

# Stage toggle buttons → update store
@app.callback(
    Output("selected-stage", "data"),
    [Input(f"stage-btn-{s}", "n_clicks") for s in stages],
    State("selected-stage", "data"),
    prevent_initial_call=True,
)
def update_stage_store(*args):
    current = args[-1]
    ctx = dash.callback_context
    if not ctx.triggered:
        return current
    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    clicked = btn_id.replace("stage-btn-", "")
    return None if current == clicked else clicked


# Capability toggle buttons → update store
@app.callback(
    Output("selected-capability", "data"),
    [Input(f"cap-btn-{c.replace(' ', '-')}", "n_clicks") for c in capabilities],
    State("selected-capability", "data"),
    prevent_initial_call=True,
)
def update_cap_store(*args):
    current = args[-1]
    ctx = dash.callback_context
    if not ctx.triggered:
        return current
    btn_id = ctx.triggered[0]["prop_id"].split(".")[0]
    clicked = btn_id.replace("cap-btn-", "").replace("-", " ")
    return None if current == clicked else clicked


# Style stage buttons (active = filled, inactive = outline)
@app.callback(
    [Output(f"stage-btn-{s}", "outline") for s in stages],
    Input("selected-stage", "data"),
)
def style_stage_buttons(selected):
    return [selected != s for s in stages]


# Style and disable capability buttons based on selected stage + active cap
@app.callback(
    [Output(f"cap-btn-{c.replace(' ', '-')}", "outline") for c in capabilities] +
    [Output(f"cap-btn-{c.replace(' ', '-')}", "disabled") for c in capabilities],
    Input("selected-capability", "data"),
    Input("selected-stage", "data"),
)
def style_cap_buttons(selected_cap, selected_stage):
    outlines = [selected_cap != c for c in capabilities]
    if selected_stage:
        # disable capabilities with weight < 2 (Low or zero) for this stage
        disabled = [
            capability_stage_weights.get(c, {}).get(selected_stage, 0) < 2
            for c in capabilities
        ]
    else:
        disabled = [False] * len(capabilities)
    return outlines + disabled


# Render metric columns
@app.callback(
    Output("metric-columns", "children"),
    Output("selection-label", "children"),
    Input("selected-stage", "data"),
    Input("selected-capability", "data"),
)
def render_columns(selected_stage, selected_capability):
    show_score = selected_stage is not None or selected_capability is not None
    scored = score_metrics(selected_stage, selected_capability)

    grouped = group_by_category(scored)

    all_scores = [m["score"] for m in scored if m["score"] is not None]
    max_score = max(all_scores) if all_scores else 12

    cols = dbc.Row([
        make_category_column("Operational", grouped["Operational"], show_score, max_score),
        make_category_column("Structural",  grouped["Structural"],  show_score, max_score),
        make_category_column("Functional",  grouped["Functional"],  show_score, max_score),
    ], className="g-3")

    if not show_score:
        label = "Select a stage or capability above to score and rank metrics."
    else:
        parts = []
        if selected_stage:
            parts.append(f"Stage: {selected_stage}")
        if selected_capability:
            parts.append(f"Capability: {selected_capability}")
        label = [
            html.Strong("Scoring by: "),
            " + ".join(parts),
            " — metrics ranked by relevance within each category. Higher score = more relevant.",
        ]

    return cols, label


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("Supply Chain Resilience Framework Dashboard")
    print("="*80)
    print("Open your browser to: http://127.0.0.1:8050/")
    print("Press Ctrl+C to stop\n")
    import threading, webbrowser
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8050")).start()
    app.run(debug=False, host="0.0.0.0", port=8050)