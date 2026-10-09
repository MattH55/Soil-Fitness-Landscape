# Headless chart probe

```
cd scripts/browsertest && npm i puppeteer-core@22
node probe.js                      # probes dist/index.html
node probe.js "https://<host>/"    # or a deployed copy
```
Clicks every indicator and every tab, checks each Plotly chart drew SVG paths, toggles dark
mode, checks for horizontal overflow at phone width, and writes one PNG per tab. Expect
`0 failing charts; 0 errors`. Uses Chrome at `C:/Program Files/Google/Chrome/Application/chrome.exe`.
