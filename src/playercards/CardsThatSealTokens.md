# Library for Cards That Seal Tokens

This file provides options for cards to seal tokens in their context menu. All cards are automatically given the option to release a single token (e.g., for "Hallow" and "A Watchful Peace") and to release all sealed tokens (e.g., when a card leaves play).

When more than three token types are eligible to be sealed, the context menu shows one **Seal token...** entry that opens a token-choice dialog instead of listing each type separately. The dialog refreshes bag contents first when `UPDATE_ON_HOVER` is enabled. `KEEP_OPEN` also applies to the grouped menu entry.

**Note:** The options below must be set on the card before this file is `require`d.

---

## Configuration Options

### `MAX_SEALED`
* **Type:** `number`
* **Description:** The maximum number of tokens this card can seal. This is **required** for all cards.
* **Details:**
    * If `MAX_SEALED` is greater than 1, a label will appear on the topmost sealed token to indicate the total count.
    * The system will throw an error if a user tries to seal more tokens than the `MAX_SEALED` value.
* **Example:** `The Chthonian Stone` allows only one token.
```lua
MAX_SEALED = 1
```

### `UPDATE_ON_HOVER`
* **Type:** `boolean`
* **Description:** If `true`, the context menu options will be automatically updated whenever the card is hovered over. This is useful for displaying only valid tokens. The "Read Bag" function is used to check the contents of the chaos bag.
* **Example:** `Unrelenting` uses this to only display valid token options.

### `KEEP_OPEN`
* **Type:** `boolean`
* **Description:** Keeps the context menu open after an option is selected. This is useful for cards that seal multiple tokens one at a time.
* **Example:** `Unrelenting` uses this to allow multiple selections.

### `SHOW_MULTI_RELEASE`
* **Type:** `number`
* **Description:** Enables a context menu entry to release multiple tokens at once, up to the number specified. The function will not fail if fewer than the maximum number of tokens are sealed.
* **Example:** `Nephthys` uses this to release up to 3 bless tokens at once.
```lua
SHOW_MULTI_RELEASE = 3
```

### `SHOW_MULTI_RETURN`
* **Type:** `number`
* **Description:** Enables a context menu entry to return a specified number of tokens to the token pool. This will fail if not enough tokens are sealed.
* **Example:** `Nephthys` uses this to return 3 bless tokens at once.
```lua
SHOW_MULTI_RETURN = 3
```

### `SHOW_RETURN_ALL`
* **Type:** `boolean`
* **Description:** Enables a context menu entry to return all sealed tokens to the token pool, regardless of how many there are.
* **Example:** `Radiant Smite` uses this to return all sealed bless tokens.

### `SHOW_MULTI_SEAL`
* **Type:** `number`
* **Description:** Enables a context menu entry to seal multiple tokens at once, up to the number specified.
* **Example:** `Holy Spear` uses this to seal two bless tokens at once.
```lua
SHOW_MULTI_SEAL = 2
```

### `VALID_TOKENS`
* **Type:** `table`
* **Description:** A table that defines which tokens are valid to be sealed. You must define this for every card, even if the table is empty.
* **Example:** `The Chthonian Stone` can seal specific tokens.
```lua
VALID_TOKENS = {
  ["Skull"]       = true,
  ["Cultist"]     = true,
  ["Tablet"]      = true,
  ["Elder Thing"] = true
}
```

### `INVALID_TOKENS`
* **Type:** `table`
* **Description:** A table that defines which tokens are invalid for sealing. This only needs to be defined if necessary, and is often used in combination with an empty `VALID_TOKENS` table.
* **Example:** `Protective Incantation` uses this to disallow sealing the "Auto-fail" token.
```lua
INVALID_TOKENS = {
  ["Auto-fail"] = true
}
```

---

## Usage Examples

### Example 1: `Crystalline Elder Sign`

This card can only seal the `+1` or `Elder Sign` token, and doesn't need specific options for multi-sealing or releasing.

```lua
VALID_TOKENS = {
  ["+1"]         = true,
  ["Elder Sign"] = true
}
MAX_SEALED = 1
require('path/to/sealing_library')
```

### Example 2: `Holy Spear`

This card features two relevant abilities: releasing a single `Bless` token and sealing two `Bless` tokens.

```lua
VALID_TOKENS = {
  ["Bless"] = true
}
SHOW_MULTI_SEAL = 2
MAX_SEALED = 10
require('path/to/sealing_library')
```