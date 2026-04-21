# Workflow Checklists

Use this reference to recommend or audit EEG signal-quality workflows. Always adapt steps to the analysis goal; preprocessing that is good for one paradigm can erase the signal in another.

## Pre-Decision Checklist

1. Define the target signal: paradigm, labels, expected time window, frequency band, channels, and output metric.
2. Confirm recording basics: montage, reference, ground, sampling rate, filter history, event markers, impedance, auxiliary channels.
3. Inspect raw data before heavy filtering: look for clipping, flatlines, pops, dropouts, reference failure, and gross movement.
4. Inspect PSD and spectrogram: line noise, EMG, SSVEP bins, alpha/mu/beta, sudden nonstationarity.
5. Inspect topographies: expected neural fields vs single-electrode or edge artifacts.
6. Compare with events and sensors: EOG, ECG, EMG, accelerometer, respiration, video, stimulus/trigger logs.
7. Decide preserve/correct/reject/interpolate with the downstream model in mind.

## Raw Waveform Visual Inspection

Flag likely:

- Blink: large frontopolar slow transient with posterior falloff.
- Saccade: lateral frontal polarity reversal or step-like gaze shift.
- EMG: dense high-frequency spiky burst, often temporal/frontal.
- ECG: regular sharp/pulse-like recurrence matching heart rate.
- Sweat: very slow baseline sway.
- Electrode pop: abrupt single-electrode transient or step.
- Flat/dropout: constant/repeated samples or timestamp gap.
- Clipping: plateaus at hardware extrema.
- Reference failure: simultaneous implausible disturbance across many channels.

Do not flag solely because:

- A sleep feature is high amplitude.
- A P300 is a large positive averaged component.
- MI produces central mu/beta ERD/ERS.
- SSVEP creates harmonics at stimulus-related bins.
- A benign variant is sharply contoured in clinical EEG.

## Bad-Channel Workflow

1. Detect unusable channels first: NaN, no-data/flatline, clipping, extreme dropout.
2. Check high-noise channels: robust variance, HF-noise ratio, line-noise ratio.
3. Check low-SNR channels: poor correlation/predictability with neighbors or RANSAC-predicted time course.
4. Check bridged electrodes: unusually high correlation between nearby channels.
5. Check reference dependency: a bad reference can make many channels look bad.
6. Mark bad channels before ICA if they are severe; interpolate after robust reference when appropriate.
7. Report number and location of removed/interpolated channels.

## Epoch Rejection Workflow

- Use peak-to-peak and robust window statistics to find gross artifacts.
- Inspect condition-wise rejection rates; differential rejection can bias ERP/BCI results.
- For P300/ERP, preserve enough target trials and report baseline variance.
- For MI, reject actual movement/EMG bursts but avoid rejecting weak ERD trials just because amplitude is low.
- For SSVEP, reject windows with blinks/motion but verify rejection does not selectively remove one target frequency.
- For sleep/clinical EEG, epoch rejection must respect state/stage and clinical review needs.

## ICA / ICLabel Workflow

Use when:

- Enough channels and data length support stable ICA.
- Artifacts are stereotyped: blinks, saccades, ECG, EMG, line noise.
- The analysis benefits from preserving trials rather than rejecting them.

Check each component:

- Scalp map: dipolar plausible brain source vs frontal eye/edge muscle/noisy channel.
- Spectrum: alpha/mu/beta brain rhythm vs broadband EMG vs line peak.
- Time course: event/state relation, blink/ECG/movement correlation.
- ICLabel probabilities: brain, muscle, eye, heart, line noise, channel noise, other.

Do not:

- Delete components only by label probability when the component contains target signal.
- Run ICA on data with severe bad channels left in.
- Interpret ICA classes as clinical diagnosis.

## ASR Workflow

Use when:

- Continuous data contain transient high-amplitude artifacts.
- Mobile/wearable or movement-rich recordings need automated correction.
- A clean calibration segment can be identified or estimated.

Check:

- Calibration segment quality.
- Cutoff aggressiveness and amount of data reconstructed.
- Whether ASR attenuates target evoked or rhythmic activity.
- Before/after PSD, ERP/SSVEP/MI feature preservation.

Avoid:

- Overly strict ASR that removes task-relevant movement-related or sleep-state signals.
- Using ASR as a substitute for documenting acquisition problems.

## Autoreject Workflow

Use when:

- Epoched EEG/MEG needs data-driven peak-to-peak thresholds.
- Local repair of bad sensors within trials is preferable to dropping full epochs.

Check:

- Cross-validated thresholds.
- Number of repaired sensors per trial.
- Dropped trials by condition.
- Whether interpolation is reasonable for electrode density.

## PREP-Inspired Early Processing

Use this logic for large or heterogeneous datasets:

1. Remove or model line noise before broad filtering choices if high-frequency preservation matters.
2. Estimate a robust reference so bad channels do not contaminate ordinary average reference.
3. Detect bad channels relative to the robust reference.
4. Interpolate bad channels while retaining records of what was changed.
5. Keep enough metadata to re-reference or reproduce processing.

## FASTER-Inspired Statistical Screening

Use this logic for automated QC:

- Detect outlier channels, epochs, and components with statistical measures.
- Include channel variance, correlation, Hurst or trend measures, kurtosis, and ICA-component features where available.
- Validate automated flags against raw examples.
- Report sensitivity/specificity only if ground truth or expert labels exist.

## Paradigm-Specific Preservation Rules

### P300 / ERP

- Preserve parietal/central positivity around 250-500 ms when it is target-related and baseline-corrected.
- Check that apparent P300 is not caused by target-locked blinks or trigger leakage.
- Avoid high-pass filters that distort component latency/onset.

### MI / SMR

- Preserve central mu/beta ERD/ERS even if amplitude is modest.
- Reject or correct actual movement and jaw/neck EMG that changes beta/gamma power.
- Do not treat posterior alpha suppression as MI unless it localizes and times like sensorimotor activity.

### SSVEP / SSMVEP

- Preserve stimulus-frequency peaks and harmonics over occipital channels.
- Audit target frequencies against 50/60 Hz and harmonics before applying notch filters.
- Confirm phase/frequency locking and topography rather than relying on one PSD peak.

### Sleep / Clinical

- Preserve stage-defining waveforms and normal variants unless the task specifically asks for artifact-only cleaning.
- Do not label sharp normal variants as artifacts or pathology without clinical context.
- Use ECG, respiration, video, and montage review for artifact confirmation.

### Mobile / Wearable

- Expect more motion, jaw, cable, and dropout artifacts.
- Use accelerometer/device logs whenever available.
- Prefer transparent annotations and before/after feature preservation checks.

## Final Recommendation Template

```text
Workflow:
1. Immediate checks:
2. Candidate artifacts/noise:
3. Features to compute:
4. Cleaning/annotation:
5. Preserve-risk checks:
6. Report fields:
```
