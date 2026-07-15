# Task: Fix Page Header Dark Mode and RTL/LTR Alignment

## Changes Made:
1. Removed hardcoded 'bg-color-light-scale-1' and 'text-dark' classes from 404, 500, and terms HTML templates.
2. Added 'custom-dynamic-header' class to relevant sections.
3. Implemented robust CSS in 'custom.css' to handle Dark Mode switching with a Pistachio Green accent (#93c572).
4. Overrode Bootstrap's 'text-md-right' dynamically based on HTML 'dir' attribute to fix LTR/RTL Flexbox alignment bugs.