# Discrimination Features

Use this reference when a judgment needs numeric or semi-quantitative evidence. Prefer robust, dataset-relative thresholds over universal cutoffs because EEG amplitude and noise depend on montage, reference, device, subject, and task.

For distribution-level comparisons of clean EEG, artifacts, and noise, load `references/statistical-distribution-atlas.md` first. This file defines the individual features; the statistical-distribution atlas explains how feature values should differ across classes, windows, trials, channels, and ICA components.

## Feature Families

### Amplitude And Peak-To-Peak

- Use for: gross artifacts, epoch rejection, clipping detection, ERP amplitude after averaging.
- Evidence patterns:
  - EOG and EMG can be orders of magnitude larger than small ERP effects.
  - Single-epoch peak-to-peak thresholds catch large transient artifacts but can remove rare high-amplitude neural events.
  - Clipping appears as repeated exact maxima/minima and flat plateaus.
- Avoid: using amplitude alone to classify artifact; slow cortical potentials and sleep waves can be high amplitude.

### Baseline Drift And Low-Frequency Trend

- Use for: sweat, electrode drift, respiration, slow movement, DC instability.
- Evidence patterns:
  - Very slow changes below typical ERP bands.
  - Large baseline differences between pre-stimulus windows.
  - Drift correlated with temperature, sweating, posture, or impedance.
- Avoid: aggressive high-pass filtering when analyzing slow cortical potentials, CNV, sleep slow waves, or clinical delta.

### PSD, Bandpower, And Spectral Shape

- Use for: resting rhythms, MI/SMR, SSVEP, EMG, line noise, workload, sleep.
- Evidence patterns:
  - Clean alpha/mu/beta should have plausible scalp topography and state/task reactivity.
  - EMG is broadband high-frequency and often temporalis/frontal.
  - Line noise is narrow at 50/60 Hz and harmonics.
  - SSVEP is narrow at stimulus frequency and harmonics over occipital areas.
- Avoid: treating all high-frequency power as neural gamma without muscle checks.

### SNR And SNRD

- Use for: evoked/steady-state responses, wearable EEG, before/after cleaning reports.
- Evidence patterns:
  - SSVEP SNR: power at stimulus bin relative to neighboring bins.
  - ERP SNR: component amplitude relative to baseline variance or non-target condition.
  - SNR deterioration can quantify artifact impact under controlled artifact tasks.
- Avoid: comparing SNR across incompatible references/filters without documenting preprocessing.

### ERP Amplitude And Latency

- Use for: P300, VEP/AEP/SEP, ErrP/ERN/FRN, RSVP.
- Evidence patterns:
  - P300: positive target-related component often around 250-500 ms, commonly parietal/central.
  - ERN/FRN: frontocentral negativity locked to response or feedback.
  - VEP/AEP/SEP: modality-specific latency/topography and repeatability.
- Avoid: calling a raw-trace deflection an ERP without event-locked averaging or single-trial ERP evidence.

### Line-Noise Ratio

- Use for: power-line contamination and harmonics.
- Evidence patterns:
  - Narrow peak exactly at mains frequency, often with harmonics.
  - Worsens with high impedance or poor ground.
  - Broadly present across channels or concentrated in bad channels.
- Avoid: removing a frequency that is an SSVEP target or task-relevant stimulation frequency without a plan.

### HF-Noise Ratio

- Use for: EMG, bad channel, high-frequency device noise.
- Evidence patterns:
  - Ratio of high-frequency to low-frequency robust dispersion or power.
  - Temporalis/forehead localization suggests EMG; isolated channel suggests bad electrode.
- Avoid: assuming all high HF ratio is artifact in studies targeting gamma; require topography and task checks.

### Distribution Shape: Kurtosis, Skewness, Entropy

- Use for: outlier segments, ICA component screening, non-Gaussian bursts, bad channels.
- Evidence patterns:
  - High kurtosis often flags spikes/bursts/pops.
  - Low entropy or repeated values can flag flatline/dropout.
  - High entropy plus poor correlation may indicate random channel noise.
- Avoid: rejecting solely on statistical outlier status; rare but valid responses may be non-Gaussian.

### Autocorrelation And Periodicity

- Use for: ECG, respiration, line noise, SSVEP, rhythmic artifacts.
- Evidence patterns:
  - ECG: regular recurrence matching heart rate and QRS timing.
  - SSVEP: stable periodic response tied to stimulus frequency.
  - Respiration: slow periodicity matching breathing.
- Avoid: confusing periodic neural rhythms with external periodic noise without spatial/event evidence.

### Channel Correlation, Coherence, And Predictability

- Use for: bad channels, bridging, robust reference, RANSAC-style quality detection.
- Evidence patterns:
  - Very high correlation between neighbors can indicate bridging.
  - Low correlation/predictability relative to neighboring channels suggests bad/noisy channel.
  - Broad common correlation can reflect reference/ground problem.
- Avoid: applying the same criteria to very low-density montages without caution.

### Robust Z-Score And Outlier Windows

- Use for: automated channel/window screening.
- Evidence patterns:
  - Median/IQR-based z-scores are less distorted by extreme channels.
  - Compute over channels and over short windows to separate global events from local failure.
- Avoid: fixed thresholds without reviewing the flagged examples and task relevance.

### ICA And ICLabel Evidence

- Use for: separating brain, muscle, eye, heart, line noise, channel noise, and other components.
- Evidence patterns:
  - Eye IC: frontal topography, blink-like time course, low-frequency power.
  - Muscle IC: edge/temporal topography, broadband high-frequency spectrum.
  - Heart IC: ECG-locked time course.
  - Line-noise IC: narrow frequency peak.
  - Brain IC: dipolar scalp map, plausible spectrum, task-related activation.
- Avoid: deleting ICs automatically without checking whether task signal is represented in the component.

## Paradigm-Specific Feature Suitability

| Feature | ERP/P300 | MI/SMR | SSVEP | Continuous/mobile | Clinical/sleep |
| --- | --- | --- | --- | --- | --- |
| Amplitude/peak-to-peak | good for epoch QC | catches movement bursts | catches gross motion | useful but crude | must be state-aware |
| PSD/bandpower | baseline/noise check | primary feature | primary feature | key feature | key feature |
| SNR/SNRD | ERP SNR | less direct | primary measure | useful for reports | context-dependent |
| ERP latency/amplitude | primary feature | not primary | not primary | only event tasks | evoked studies only |
| Line-noise ratio | important | important | critical if overlap | important | important |
| HF-noise ratio | EMG screen | critical for jaw/neck EMG | eye/muscle screen | critical | sleep muscle state-aware |
| Channel correlation | bad-channel/bridging | spatial filters affected | bad occipital channels | critical | montage-dependent |
| ICA/ICLabel | common | useful with enough channels | useful, but avoid SSVEP deletion | useful if data supports ICA | clinical caution |
| ASR window statistics | use before ERP cautiously | useful for movement bursts | useful if preserving frequency bins | often useful | must preserve state features |

## Practical Evidence Bundles

### Clean Neural Signal Bundle

- Matches expected paradigm timing/frequency/topography.
- Repeats across trials, blocks, or subjects in plausible ways.
- Shows contrast with control condition or baseline.
- Is not better explained by EOG/EMG/ECG/movement/reference evidence.

### Ocular Artifact Bundle

- Frontal maximum, EOG correlation, blink/saccade morphology.
- Low-frequency dominance or lateral frontal polarity reversal.
- Timing linked to visual task, fatigue, or response.

### Muscle Artifact Bundle

- Broadband high-frequency burst, temporal/frontal/neck topography.
- Short spiky morphology, condition linked to speech, jaw, effort, movement.
- ICA muscle component or EMG/video confirmation.

### Bad Channel Bundle

- Isolated extreme variance, flatline, low predictability, NaNs, clipping, dropout.
- Not consistent with physiological scalp field.
- Persists across task conditions or changes abruptly with impedance.

### Line Noise Bundle

- Narrow peak at mains frequency/harmonics.
- Present across many channels or amplified in high-impedance channels.
- No task-locked topography matching neural target.

## Reporting Template

Use this concise feature report when needed:

```text
Feature evidence:
- Time domain:
- Frequency domain:
- Spatial/topographic:
- Event/state locking:
- Cross-channel:
- External sensors/logs:
- Numeric QC:
Conclusion:
```
