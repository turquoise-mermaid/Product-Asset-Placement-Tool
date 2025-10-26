# Asset Placement Tool

Batch processes design files into multiple product sizes for Print-on-Demand.

## What It Does

Converts your design files into 6 product formats:
- Stickers (1250×1250px @ 300 DPI)
- Mugs (1250×1250px @ 300 DPI)
- T-Shirts (3375×3375px @ 300 DPI)
- Pillows (4000×4000px @ 150 DPI)
- Posters (2400×3000px @ 300 DPI)
- 300 DPI versions (original size @ 300 DPI)

## Requirements

- Python 3.8+
- Pillow (PIL)

## How to Run

```bash
pip install -r requirements.txt
python asset_placement_tool.py
```

## Customization

Default sizes are based on Printful specs. To customize for other platforms, edit the `product_specs` dictionary in lines 26-33.

## Support

Contact via Gumroad messaging after purchase.
