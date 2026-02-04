# Changelog

## Version 3.1.0 - Pixel-Perfect Alignment (February 4, 2026)

### Summary
Achieved pixel-perfect right-edge alignment of all job locations and dates at X=588, ensuring a clean, professional, and visually consistent CV layout.

### Major Achievement: Right-Edge Alignment at X=588

All 7 job locations and 7 job dates now terminate precisely at X=588 (right edge alignment):

**Jobs with aligned locations and dates:**
1. JOBSITY
2. ZENTA GROUP
3. DEUNA
4. SPOT
5. EPAM Systems
6. WALMART Chile
7. LAMNGEN Ltda.

### Alignment Methodology

**Iterative Refinement Process:**
- Initial target: X=590
- Refined to: X=589
- Final precision: X=588

**Key Techniques:**
- Font metric-based width calculations
- Micro-adjustments in 0.1-0.2 point increments
- Visual reference line for verification (removed in final version)
- Precision corrector offset consideration (+1.5 for dates)

### Final Coordinate Adjustments

**Location Coordinates (X positions):**
- Zenta Group: 524.87
- Walmart Chile: 530.99
- Lamngen Ltda: 526.29
- Spot: 533.4

**Date Coordinates (X positions):**
- Zenta Group: 464.75
- Deuna: 461.22
- Walmart Chile: 453.82
- Lamngen Ltda: 462.84
- EPAM Systems: 487.05
- Spot: 455.38

### Files Modified

1. **data/coordinates.json**
   - Fine-tuned X coordinates for all 7 job locations
   - Fine-tuned X coordinates for all 7 job dates
   - Maintained all Y coordinates unchanged

2. **src/renderer.py**
   - Removed debug reference line (cleanup)

### Verification

- ✅ All 7 locations right-aligned at X=588
- ✅ All 7 dates right-aligned at X=588
- ✅ Perfect visual consistency
- ✅ No vertical position changes
- ✅ PDF generates flawlessly
- ✅ All 157 coordinate elements validated
- ✅ All 5 shape elements validated

### Technical Notes

**Alignment Target**: X=588 (right edge)
**Precision Level**: 0.1 point increments
**Total Elements Aligned**: 14 (7 locations + 7 dates)
**Coordinate System**: PDF points (1/72 inch)

---

## Version 3.0.1 - Header Alignment and Link Fix (February 4, 2026)

### Summary
Fine-tuned section header positions and fixed GitHub hyperlink disambiguation logic.

### Changes Made

#### 1. Section Header Alignment
- **EDUCATION**: Moved 1 point left (X: 92.63 → 91.63)
- **EXPERIENCE**: Moved 1 point down (Y: 113.94 → 114.94)
- **PAPERS & WORKSHOPS**: Moved 4 points left (X: 72.33 → 68.33)
- **SKILLS**: Moved 3 points left (X: 108.37 → 105.37)
- **LANGUAGES**: Moved 3 points left (X: 92.97 → 89.97)

#### 2. JOBSITY Position
- **Company Name**: Y: 135.69 → 134.69
- **Job Title**: Y: 148.69 → 147.69

#### 3. GitHub Link Fix
Updated `THRESHOLD_LINK_DISAMBIGUATION_Y` in `src/config.py`:
```python
THRESHOLD_LINK_DISAMBIGUATION_Y: float = 165.0  # was 150.0
```

### Files Modified
1. **data/coordinates.json** - Header and JOBSITY positions
2. **src/config.py** - Link disambiguation threshold
3. **README.md** - Added CV preview and notes

### Verification
- ✅ All section headers properly aligned
- ✅ GitHub link correctly opens GitHub profile
- ✅ LinkedIn link correctly opens LinkedIn profile

---

**Author**: Nicolás Fredes Franco  
**Latest Version**: 3.1.0  
**Last Updated**: February 4, 2026

