fileInput.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 1. Reset UI to 'Processing' state
    isProcessing = true;
    terminal.innerHTML = '';
    percentText.innerText = '0.0';
    circle.style.strokeDashoffset = '753.98'; // Reset circle
    verdictText.innerText = 'ANALYZING...';
    verdictText.className = "text-3xl font-bold tracking-tighter uppercase text-cyan-400 animate-pulse";
    
    addLog(`> [SYSTEM] TARGET: ${file.name.toUpperCase()}`);
    addLog(`> [AI] INITIALIZING NEURAL SCAN...`);

    const formData = new FormData();
    formData.append('file', file);

    try {
        // 2. Call the Real Backend
        const response = await fetch('/api/analyze', { method: 'POST', body: formData });
        const data = await response.json();

        if (data.success) {
            // 3. Show "Processing" logs to make it feel real
            addLog(`> [SCAN] PERFORMING ELA ANALYSIS...`);
            await new Promise(r => setTimeout(r, 800));
            addLog(`> [SCAN] CHECKING METADATA FLAGS...`);
            
            // 4. Update the Gauge (Circular Shape)
            animateGauge(data.confidence); 

            // 5. Update Verdict & Logs
            setTimeout(() => {
                updateUI(data);
                // Print each flag found in the backend
                data.all_flags.forEach(flag => {
                    addLog(`> [FLAG] ${flag}`);
                });
            }, 1000);
        }
    } catch (err) {
        addLog(`> [FATAL] CONNECTION_ERROR: Check if app.py is running.`);
        verdictText.innerText = 'OFFLINE';
    } finally {
        isProcessing = false;
    }
};

function animateGauge(target) {
    let curr = 0;
    const interval = setInterval(() => {
        if (curr >= target) {
            curr = target;
            clearInterval(interval);
        } else {
            curr += 1.5;
        }
        percentText.innerText = curr.toFixed(1);
        // Correct math for r=120 (Circumference ~753.98)
        circle.style.strokeDashoffset = 753.98 - (curr / 100) * 753.98;
    }, 20);
}