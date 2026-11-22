# FOSSEE Winter Internship 2026 — OsdagBridge Task 2

## Project

**Task:** UI, 2D CAD, and plotting enhancements for OsdagBridge. This report separates the internship Task 2 deliverables from broader, incomplete OsdagBridge development.

**Repository:** https://github.com/Chandhra103/OsdagBridge

**Task 2 branch:** https://github.com/Chandhra103/OsdagBridge/tree/task2-ui-cad-transverse-plotting

**Broader development branch:** https://github.com/Chandhra103/OsdagBridge/tree/complete-osdagbridge-development

## Existing system

OsdagBridge is a Python engineering application with an existing plate-girder core and PySide6 desktop interface. Task 2 extends that desktop workflow; it does not implement or certify all broader engineering, web, or deployment requirements.

## Task 2 implementation summary

1. **Interactive 2D CAD parameter editing:** editable labels for carriageway width, girder spacing, deck thickness, and span length; derived dimensions remain read-only. Inputs are validated and synchronized with layout updates.
2. **Additional Inputs state and validation:** blank custom values are rejected; modified state is tracked and dismissal prompts for unsaved changes.
3. **Transverse result plotting:** result member selection includes end diaphragms and intermediate cross bracings. Views depend on available actual analysis data and show a no-data state when the selected result is absent. Existing longitudinal plots remain.

## Verification

The Task 2 branch's GitHub Actions run completed successfully, and the branch was published at commit `0b687d6e58507b79e4c1a841cb813821847f2e26`. On the new development branch, the pre-change baseline had 48 passing tests. The focused tests added for CLI starter-file behavior, preliminary JSON validation, and a footpath geometry correction passed 14/14. The full post-change suite must be run before finalizing this branch. Automated tests do not substitute for live GUI testing or engineering benchmark verification.

## Evidence and screenshots

No screenshots are included because no authentic GUI screenshots were captured in this execution. Do not represent source code or test output as a visual demonstration. Add actual screenshots only after capturing the application in a supported graphical environment.

## Known limitations

The desktop application requires its supported Osdag/Qt/CAD runtime and was not exhaustively exercised here. The CLI is only a JSON starter-project utility and does not run engineering analysis or produce reports. Django/React are scaffolds, not a completed web app; no deployment URL, pull request, release, or desktop package is claimed. Solver and engineering accuracy require additional reference-model verification.

## Installation and testing

See the repository `README.md` for setup and test commands. Task 2 GUI steps are summarized in `docs/user_guide.md`. The submitted implementation branch is based on the published Task 2 branch; its subsequent commits should be listed here only after they are actually pushed and verified.

## Conclusion

Task 2 contributes the CAD editing, additional-input handling, and transverse plotting improvements described above. Broader shared-core, web, deployment, packaging, and release requirements remain separate future work and are not claimed as completed by this internship task.
