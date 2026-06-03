---
name: eeg-signal-quality-atlas
description: EEG signal-quality atlas for distinguishing clean neural EEG, artifacts, and noise across resting/spontaneous EEG, clinical/sleep EEG, MI/SMR, P300/oddball ERP, SSVEP/SSMVEP, VEP/AEP/SEP, ErrP/ERN/FRN, RSVP, emotion/affective EEG, attention/workload, neurofeedback, wearable/mobile EEG, and hybrid BCI. Use when Codex needs to inspect, explain, report, or choose preprocessing for EEG clean signal vs ocular, muscle, cardiac, motion, sweat, bad-channel, line-noise, trigger-leakage, or instrumentation contamination using waveform, distribution, time-frequency, spatial, event-locked, and numerical features.
---

# EEG Signal Quality Atlas

## Overview

Use this skill as a decision atlas for separating clean EEG activity, physiological artifacts, and external/instrumental noise. Default to Chinese prose, keep EEG terms in English where they are standard, and avoid presenting signal-quality judgments as medical diagnosis.

## Reference Loading

Load only the references needed for the current task:

- Use `references/paradigm-atlas.md` when the user names or implies a paradigm such as `MI`, `P300`, `SSVEP`, sleep EEG, wearable EEG, emotion EEG, workload, or hybrid BCI.
- Use `references/artifact-noise-taxonomy.md` when the task is to identify artifact/noise source from waveform, topography, or recording context.
- Use `references/discrimination-features.md` when the task needs numeric features, thresholds, signal-quality indices, ICA/ICLabel evidence, PSD/SNR, or tabular criteria.
- Use `references/statistical-distribution-atlas.md` when the task asks about statistical distribution, 分布差异, 特征分布, amplitude distribution, PSD distribution, feature distribution, outlier distribution, robust z-score, or how clean EEG, artifacts, and noise differ in raw-amplitude, window/epoch, frequency-domain, trial/event, channel-quality, or ICA-component feature distributions.
- Use `references/workflow-checklists.md` when recommending preprocessing, inspection order, bad-channel handling, epoch rejection, ICA, ASR, Autoreject, PREP, or FASTER.
- Use `references/source-map.md` when citing literature basis, checking source provenance, or expanding the atlas.

## Core Workflow

1. Identify the analysis context: paradigm, task timing, montage/reference, channels of interest, sampling rate, filters, event markers, subject behavior, and whether the user is asking for interpretation, preprocessing, quality control, or reporting.
2. Load the relevant paradigm page first, then artifact/noise taxonomy if contamination is plausible, then feature/checklist references as needed.
3. Compare candidate explanations along seven axes:
   - Waveform morphology: spike, slow drift, sinusoid, burst, saturation, flatline, transient, rhythmic train.
   - Time-frequency pattern: delta/theta/alpha/mu/beta/gamma, broadband EMG, line-frequency peaks, stimulus-locked bins, ERD/ERS.
   - Spatial distribution: frontal, central sensorimotor, parietal, occipital, temporal, single-electrode, reference-wide, bilateral symmetry.
   - Event locking: stimulus-locked, response-locked, instruction-locked, respiration/ECG-locked, movement-locked, random.
   - Cross-channel relation: volume-conducted field, high local correlation, bridged channels, isolated bad channel, low predictability.
   - Numeric evidence: amplitude, peak-to-peak, PSD/bandpower, SNR/SNRD, kurtosis, entropy, autocorrelation, robust z-score, channel correlation, RANSAC predictability, ICA/ICLabel class.
   - Verification action: inspect raw traces, topomap, PSD, spectrogram, event averages, ECG/EOG/EMG/accelerometer/video/trigger logs, impedance, reference and ground.
4. Decide whether each component/segment/channel should be preserved, annotated, corrected, rejected, interpolated, or left for expert review.

## Output Contract

When answering an EEG signal-quality request, return a compact structured assessment:

```text
判定:
证据:
可能混淆:
建议验证:
处理建议:
保留/剔除风险:
```

For multi-class cases, use a table with columns:

`候选成分 | 更像纯净信号/伪迹/噪声 | 关键证据 | 反证或混淆 | 下一步验证 | 处理建议`

## Decision Rules

- Do not classify by amplitude alone. High-amplitude neural activity, low-amplitude artifact, and reference artifacts can all violate simple thresholds.
- Treat single-channel sharp transients, flatlines, saturations, step changes, or nonphysiological discontinuities as instrumentation candidates until proven otherwise.
- Treat frontal slow large deflections as ocular candidates, but check event timing because P300/P3a, frontal N components, and slow cortical potentials can overlap.
- Treat high-frequency temporalis/frontal bursts as EMG candidates, but check whether the analysis target includes gamma activity; EMG is usually broadband and movement-linked.
- Treat narrow peaks exactly at 50/60 Hz and harmonics as line noise candidates, but do not confuse SSVEP stimulus frequencies or harmonics with power-line contamination.
- Preserve task-relevant neural signatures unless there is independent artifact evidence: MI mu/beta ERD/ERS, P300 250-500 ms positivity, SSVEP stimulus-frequency harmonics, ErrP/ERN response-locked negativity, sleep spindles/K-complexes, and normal rhythms/benign variants.
- If uncertainty remains, report competing hypotheses and the minimum verification needed rather than forcing a binary clean/artifact label.

## Safety And Scope

Use this skill for EEG quality control, preprocessing choice, and research reporting. Do not use it to diagnose epilepsy, sleep disorders, neurodegenerative disease, psychiatric disease, or individual clinical status. For clinical EEG interpretation, label statements as signal-quality or pattern-recognition support and recommend review by qualified clinical personnel when patient care is involved.
