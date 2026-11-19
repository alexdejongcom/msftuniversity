"""Builds tools/azure/dashboard.json — the 'Microsoft University — status'
Azure portal dashboard (properties JSON for `az portal dashboard create`).
Run: python3 tools/azure/make-dashboard.py"""
import json, os, uuid

SUB = "b3a5e23d-4ccf-463a-a6bc-0a429fd415ea"
RG = f"/subscriptions/{SUB}/resourceGroups/rg-msftuniversity/providers"
SWA = RG + "/Microsoft.Web/staticSites/msftuniversity"
ACS = RG + "/Microsoft.Communication/CommunicationServices/msftuniversity-acs"
AI = RG + "/microsoft.insights/components/msftuniversity-insights"
DAY, MONTH = 86400000, 30 * 86400000

def md(x, y, w, h, title, text):
    return {"position": {"x": x, "y": y, "colSpan": w, "rowSpan": h}, "metadata": {
        "type": "Extension/HubsExtension/PartType/MarkdownPart", "inputs": [],
        "settings": {"content": {"settings": {"content": text, "title": title, "subtitle": "", "markdownSource": 1}}}}}

def metric(x, y, w, h, title, ns, rid, metrics, chart=2, span=MONTH, split=None):
    m = [{"resourceMetadata": {"id": rid}, "name": n, "aggregationType": agg, "namespace": ns,
          "metricVisualization": {"displayName": label}} for n, agg, label in metrics]
    ch = {"metrics": m, "title": title, "titleKind": 2,
          "visualization": {"chartType": chart, "legendVisualization": {"isVisible": True, "position": 2, "hideSubtitle": False},
                            "axisVisualization": {"x": {"isVisible": True, "axisType": 2}, "y": {"isVisible": True, "axisType": 1}}, "disablePinning": True},
          "timespan": {"relative": {"duration": span}, "showUTCTime": False, "grain": 1}}
    if split:
        ch["grouping"] = {"dimension": split, "sort": 2, "top": 10}
    return {"position": {"x": x, "y": y, "colSpan": w, "rowSpan": h}, "metadata": {
        "type": "Extension/HubsExtension/PartType/MonitorChartPart",
        "inputs": [{"name": "options", "isOptional": True}, {"name": "sharedTimeRange", "isOptional": True}],
        "settings": {"content": {"options": {"chart": ch}}}}}

def logs(x, y, w, h, title, query, span="P7D"):
    pid = str(uuid.uuid5(uuid.NAMESPACE_URL, title))
    inputs = [
        {"name": "resourceTypeMode", "isOptional": True}, {"name": "ComponentId", "isOptional": True},
        {"name": "Scope", "value": {"resourceIds": [AI]}, "isOptional": True},
        {"name": "PartId", "value": pid, "isOptional": True}, {"name": "Version", "value": "2.0", "isOptional": True},
        {"name": "TimeRange", "value": span, "isOptional": True}, {"name": "DashboardId", "isOptional": True},
        {"name": "DraftRequestParameters", "isOptional": True}, {"name": "Query", "value": query, "isOptional": True},
        {"name": "ControlType", "value": "AnalyticsGrid", "isOptional": True}, {"name": "SpecificChart", "isOptional": True},
        {"name": "PartTitle", "value": title, "isOptional": True}, {"name": "PartSubTitle", "value": "Application Insights", "isOptional": True},
        {"name": "Dimensions", "isOptional": True}, {"name": "LegendOptions", "isOptional": True},
        {"name": "IsQueryContainTimeRange", "value": False, "isOptional": True}]
    return {"position": {"x": x, "y": y, "colSpan": w, "rowSpan": h}, "metadata": {
        "type": "Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart",
        "inputs": inputs, "settings": {"content": {"PartTitle": title, "PartSubTitle": "Application Insights (last 7 days)"}}}}

SITE = "https://msftuniversity.com"
header = (
    "**Microsoft University — status at a glance.** Traffic and errors come from Azure itself; "
    "API details from Application Insights; newsletter delivery from Communication Services.\n\n"
    f"[Newsletter editor & subscribers]({SITE}/newsletter-admin.html) · "
    f"[Visitor map]({SITE}/visitors.html) · "
    f"[Public status page]({SITE}/status.html) · "
    "[Newsletter scheduler runs](https://github.com/alexdejongcom/msftuniversity/actions/workflows/newsletter-tick.yml) · "
    "[Deployments](https://github.com/alexdejongcom/msftuniversity/actions)")
guide = (
    "**What good looks like:** function errors near zero; no rows in *API warnings & errors*; "
    "every newsletter mail ends as *Delivered*. A *Failed* or *Suppressed* bar means an address bounced — "
    "remove it in the editor. Unsubscribed addresses are deleted instantly, so they never show up here.")

parts = [
    md(0, 0, 8, 2, "Microsoft University", header),
    md(8, 0, 4, 2, "How to read this", guide),
    metric(0, 2, 6, 4, "Site hits per day (30 days)", "microsoft.web/staticsites", SWA, [("SiteHits", 1, "Site hits")], chart=1),
    metric(6, 2, 6, 4, "API calls and errors (30 days)", "microsoft.web/staticsites", SWA,
           [("FunctionHits", 1, "API calls"), ("FunctionErrors", 1, "API errors")], chart=2),
    logs(0, 6, 6, 4, "API endpoints",
         "requests | summarize Calls=count(), Failed=countif(success == false), AvgMs=round(avg(duration)), P95Ms=round(percentile(duration, 95)) by Endpoint=name | order by Calls desc"),
    logs(6, 6, 6, 4, "API warnings & errors",
         "union (traces | where severityLevel >= 2 | project timestamp, Level=iff(severityLevel >= 3, \"Error\", \"Warning\"), Source=operation_Name, Message=message), "
         "(exceptions | project timestamp, Level=\"Exception\", Source=operation_Name, Message=outerMessage) | order by timestamp desc | take 50"),
    metric(0, 10, 6, 4, "Newsletter mail delivery (30 days)", "microsoft.communication/communicationservices", ACS,
           [("DeliveryStatusUpdate", 7, "Delivery status")], chart=1, split="MessageStatus"),
    logs(6, 10, 6, 4, "Newsletter activity per day",
         "requests | where name in (\"nlSubscribe\", \"nlConfirm\", \"nlUnsubscribe\", \"nlArchive\", \"nlIssue\", \"nlTick\", \"nlAdmin\") "
         "| extend Action=case(name == \"nlSubscribe\", \"Sign-ups\", name == \"nlConfirm\", \"Confirmations\", name == \"nlUnsubscribe\", \"Unsubscribes\", "
         "name == \"nlIssue\", \"Web views\", name == \"nlArchive\", \"Archive views\", name == \"nlTick\", \"Scheduler runs\", \"Editor actions\") "
         "| summarize Count=count() by Day=format_datetime(startofday(timestamp), \"yyyy-MM-dd\"), Action | order by Day desc, Action asc"),
    metric(0, 14, 6, 4, "Data sent (30 days)", "microsoft.web/staticsites", SWA, [("BytesSent", 1, "Bytes sent")], chart=1),
    logs(6, 14, 6, 4, "Slowest API calls",
         "requests | top 20 by duration desc | project timestamp, Endpoint=name, Ms=round(duration), Status=resultCode"),
]

props = {"lenses": [{"order": 0, "parts": parts}], "metadata": {"model": {
    "timeRange": {"value": {"relative": {"duration": 24, "timeUnit": 1}}, "type": "MsPortalFx.Composition.Configuration.ValueTypes.TimeRange"},
    "filterLocale": {"value": "en-us"}, "filters": {"value": {"MsPortalFx_TimeRange": {"model": {"format": "local", "granularity": "auto", "relative": "30d"}, "displayCache": {"name": "Local Time", "value": "Past 30 days"}}}}}}}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.json")
json.dump(props, open(out, "w"), separators=(",", ":"), ensure_ascii=False)
print(out, os.path.getsize(out), "bytes")
