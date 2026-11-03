import requests
from pathlib import Path

script_dir = Path(__file__).resolve().parent

# --- CONFIGURATION ---

ARKHAMBUILD_URL = "https://api.arkham.build/v1/cache/cards/en"
OUTPUT_PATH = script_dir / "ReprintGroups.ttslua"

DUPE_OVERRIDE = {
    # Core 2026
    "12024": "04103",  # Scene of the Crime (0)
    "12025": "01025",  # Vicious Blow (0)
    "12031": "05024",  # Fingerprint Kit (0)
    "12034": "01030",  # Magnifying Glass (0)
    "12038": "01037",  # Working a Hunch (0)
    "12039": "01039",  # Deduction (0)
    "12042": "05276",  # Studious (3)
    "12044": "04107",  # Lucky Cigarette Case (0)
    "12049": "09064",  # Thieves Kit (0)
    "12050": "07114",  # Breaking and Entering (0)
    "12056": "05278",  # Another Day, Another Dollar (3)
    "12064": "04199",  # Premonition (0)
    "12065": "01065",  # Ward of Protection (0)
    "12069": "02268",  # Fearless (2)
    "12073": "08073",  # Bandages (0)
    "12077": "05114",  # Meat Cleaver (0)
    "12078": "01079",  # Look What I found! (0)
    "12089": "01088",  # Emergency Cache (0)
    "12094": "01093",  # Unexpected Courage (0)
    "12095": "01694",  # Charisma (3)
    "12096": "01695",  # Relic Hunter (3)
    "12097": "01096",  # Amnesia
    "12100": "03040",  # Overzealous
    "12101": "01097",  # Paranoia
    # Tommy
    "60169": "01025",  # Vicious Blow (0)
    "60176": "02299",  # Vicious Blow (2)
    # Carolyn
    "60263": "02186",  # Preposterous Sketches (0)
    "60267": "01039",  # Deduction (0)
    "60275": "02150",  # Deduction (2)
    "60270": "01040",  # Magnifying Glass (1)
    # André
    "60361": "60305",  # Lockpicks (0)
    "60372": "01687",  # Lockpicks (1)
    "60379": "08057",  # The Black Fan (3)
    "60381": "54006",  # Well Connected (3)
    "60384": "08058",  # The Red Clock (5)
    # Marie
    "60455": "01063",  # Arcane Initiate (0)
    # Miguel
    "60560": "01075",  # Rabbit's Foot (0)
}

DUPE_EXTRA = {
    # Taboo Cards from Revised Core
    "01033-t": "01533-t",
    "01050-t": "01550-t",
    "01073-t": "01573-t",
    "01692-t": "05324-t",
}


def load_api_data():
    try:
        response = requests.get(ARKHAMBUILD_URL)
        response.raise_for_status()
        return response.json()["data"]["all_card"]

    except Exception as e:
        print(f"Error fetching card data: {e}")
        return None


def export_reprint_map_to_lua(card_data):
    # Dictionary to hold the groups: {id: set_of_related_ids}
    groups = {}

    def merge_group(code, dup_of):
        group_a = groups.get(code, {code})
        group_b = groups.get(dup_of, {dup_of})
        union_group = group_a.union(group_b)

        for member in union_group:
            groups[member] = union_group

    for entry in card_data:
        code = entry["code"]

        if code in DUPE_OVERRIDE:
            entry["duplicate_of_code"] = DUPE_OVERRIDE[code]

        if "duplicate_of_code" not in entry or "taboo_set_id" in entry:
            continue

        dup_of = entry["duplicate_of_code"]

        # Union-Find logic: Merge sets so all related IDs are in one group
        merge_group(code, dup_of)

    for code, dup_of in DUPE_EXTRA.items():
        merge_group(code, dup_of)

    # Generate Lua Table string
    lua_lines = [
        "-- Reprint Data (used as basis for the fallback system for language packs)",
        "REPRINT_GROUPS = {",
    ]

    for card_id in sorted(groups.keys()):
        # Convert set to list and sort so the 'Original' IDs typically come first
        siblings = sorted(list([m for m in groups[card_id] if m != card_id]))
        siblings_str = ", ".join([f'"{s}"' for s in siblings])
        lua_lines.append(f'  ["{card_id}"] = {{ {siblings_str} }},')

    lua_lines.append("}")

    # Write to file
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(lua_lines) + "\n")

    print(f"Successfully exported to {OUTPUT_PATH}")


def main():
    card_data = load_api_data()
    export_reprint_map_to_lua(card_data)


if __name__ == "__main__":
    main()
