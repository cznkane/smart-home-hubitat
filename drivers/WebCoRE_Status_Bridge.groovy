// HPM-managed source: cznkane/smart-home-hubitat
metadata {
    definition(
        name: "WebCoRE Status Bridge",
        namespace: "rick",
        author: "Rick"
    ) {
        capability "Actuator"

        attribute "eveningDue", "string"
        attribute "duskStarted", "string"

        attribute "rickPresent", "string"
        attribute "andiePresent", "string"
        attribute "sadiePresent", "string"
        attribute "everlyPresent", "string"
        attribute "guestPresent", "string"

        command "TIME_Evening", [[name: "value", type: "STRING"]]
        command "TIME_Dusk", [[name: "value", type: "STRING"]]

        command "PRES_Rick", [[name: "value", type: "STRING"]]
        command "PRES_Andie", [[name: "value", type: "STRING"]]
        command "PRES_Sadie", [[name: "value", type: "STRING"]]
        command "PRES_Everly", [[name: "value", type: "STRING"]]
        command "PRES_Guest", [[name: "value", type: "STRING"]]
    }
}

def installed() { initialize() }
def updated() { initialize() }

def initialize() {
    if (device.currentValue("eveningDue") == null) {
        sendEvent(name: "eveningDue", value: "Not set")
    }
    if (device.currentValue("duskStarted") == null) {
        sendEvent(name: "duskStarted", value: "Not set")
    }
    ["rickPresent", "andiePresent", "sadiePresent", "everlyPresent", "guestPresent"].each { attr ->
        if (device.currentValue(attr) == null) {
            sendEvent(name: attr, value: "Unknown")
        }
    }
}

def TIME_Evening(String value) {
    def displayValue = formatTime(value)
    sendEvent(name: "eveningDue", value: displayValue,
              descriptionText: "eveningDue is ${displayValue}")
}

def TIME_Dusk(String value) {
    def displayValue = formatTime(value)
    sendEvent(name: "duskStarted", value: displayValue,
              descriptionText: "duskStarted is ${displayValue}")
}

def PRES_Rick(String value) { sendPresenceEvent("rickPresent", value) }
def PRES_Andie(String value) { sendPresenceEvent("andiePresent", value) }
def PRES_Sadie(String value) { sendPresenceEvent("sadiePresent", value) }
def PRES_Everly(String value) { sendPresenceEvent("everlyPresent", value) }
def PRES_Guest(String value) { sendPresenceEvent("guestPresent", value) }

private void sendPresenceEvent(String attributeName, String value) {
    String raw = value == null ? "" : value.trim()
    String normalized

    if (raw.equalsIgnoreCase("true") ||
        raw.equalsIgnoreCase("present") ||
        raw.equalsIgnoreCase("home") ||
        raw.equalsIgnoreCase("on") ||
        raw == "1") {
        normalized = "Present"
    }
    else if (raw.equalsIgnoreCase("false") ||
             raw.equalsIgnoreCase("not present") ||
             raw.equalsIgnoreCase("away") ||
             raw.equalsIgnoreCase("off") ||
             raw == "0") {
        normalized = "Away"
    }
    else {
        normalized = raw ?: "Unknown"
    }

    sendEvent(
        name: attributeName,
        value: normalized,
        descriptionText: "${attributeName} is ${normalized}"
    )
}

private String formatTime(String value) {
    if (!value) return "Not set"

    String raw = value.trim()

    // Extract the clock portion exactly as WebCoRE supplied it.
    // Examples:
    // Sat, Oct 3 2026 @ 5:37:58 PM CDT -> 5:37 PM
    // 8:07:58 PM CDT                  -> 8:07 PM
    // 10/1/2026 6:45 PM               -> 6:45 PM
    def matcher = raw =~ /(?i)(\d{1,2}):(\d{2})(?::\d{2})?\s*(AM|PM)/

    if (matcher.find()) {
        return "${matcher.group(1)}:${matcher.group(2)} ${matcher.group(3).toUpperCase()}"
    }

    log.warn "Could not format datetime '${value}', displaying original value"
    return value
}
