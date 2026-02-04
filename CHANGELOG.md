# Changelog - February 4, 2026

## Version 3.0.1 - Header Alignment and Link Fix

### Summary
This update includes fine-tuned adjustments to section header positions and a critical fix for the GitHub hyperlink disambiguation logic.

### Changes Made

#### 1. Section Header Alignment Adjustments
Precise horizontal and vertical positioning adjustments to improve visual alignment:

- **EDUCATION**: Moved 1 point left (X: 92.63 → 91.63)
- **EXPERIENCE**: Moved 1 point down (Y: 113.94 → 114.94)
- **PAPERS & WORKSHOPS**: Moved 4 points left total (X: 72.33 → 68.33)
  - Incremental adjustments: -1pt, -1pt, -1pt, -1pt
- **SKILLS**: Moved 3 points left (X: 108.37 → 105.37)
  - Incremental adjustments: -2pt, -1pt
- **LANGUAGES**: Moved 3 points left (X: 92.97 → 89.97)
  - Incremental adjustments: -1pt, -1pt, -1pt

#### 2. JOBSITY Position Adjustment
Moved company name and job title up by 1 point to restore optimal spacing:

- **Company Name**: Y: 135.69 → 134.69
- **Job Title**: Y: 148.69 → 147.69

#### 3. GitHub Link Fix
**Problem**: The GitHub link was incorrectly resolving to LinkedIn due to an improperly configured spatial disambiguation threshold.

**Root Cause**: 
- GitHub link Y-coordinate: 158.27
- LinkedIn link Y-coordinate: 169.27
- Previous threshold: 150.0 (both links fell above threshold → both resolved to LinkedIn)

**Solution**: Updated `THRESHOLD_LINK_DISAMBIGUATION_Y` in `src/config.py`:
```python
THRESHOLD_LINK_DISAMBIGUATION_Y: float = 165.0  # was 150.0
```

**Result**: Links now correctly disambiguate:
- Y < 165.0 → GitHub (https://github.com/nicolasfredesfranco)
- Y ≥ 165.0 → LinkedIn (http://www.linkedin.com/in/nicolasfredesfranco)

### Files Modified

1. **data/coordinates.json**
   - Updated X/Y coordinates for section headers
   - Updated JOBSITY company and title positions

2. **src/config.py**
   - Updated `THRESHOLD_LINK_DISAMBIGUATION_Y` from 150.0 to 165.0

3. **README.md**
   - Added CV preview section with latest version screenshot
   - Added note about optimized header alignment and corrected GitHub link

### Verification

- ✅ All section headers properly aligned
- ✅ GitHub link correctly opens GitHub profile
- ✅ LinkedIn link correctly opens LinkedIn profile
- ✅ PDF generates without errors
- ✅ All 157 coordinate elements validated
- ✅ All 5 shape elements validated

### Technical Details

**Coordinate System**: PDF coordinate space with origin at bottom-left
- X-axis: Increases rightward (subtract to move left, add to move right)
- Y-axis: Increases upward (subtract to move up, add to move down)

**Precision**: All adjustments made in 1-point increments for fine control

### Testing Performed

1. Generated CV with all adjustments
2. Verified GitHub link opens correct URL
3. Verified LinkedIn link opens correct URL
4. Verified visual alignment of all section headers
5. Confirmed no unintended changes to other elements

---

**Author**: Nicolás Fredes Franco  
**Date**: February 4, 2026  
**Version**: 3.0.1
