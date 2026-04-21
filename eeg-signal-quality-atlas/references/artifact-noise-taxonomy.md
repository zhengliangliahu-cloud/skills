# Artifact And Noise Taxonomy

Use this reference to identify likely contamination sources. Separate physiological artifacts from external/instrumental noise because prevention, correction, and interpretation differ.

## Top-Level Classes

| Class | Source | Typical evidence | Common action |
| --- | --- | --- | --- |
| Clean neural EEG | Brain activity of interest or background rhythms | plausible topography, event/state relation, repeatability, physiologic frequency content | preserve and model |
| Physiological artifact | Body but not brain source | EOG/EMG/ECG/respiration/sweat/motion timing, stereotyped distribution | annotate, regress/ICA/ASR/reject if harmful |
| External/instrumental noise | electrode, amplifier, cable, environment, trigger, software | single-channel failure, line peaks, discontinuity, clipping, dropout, reference-wide issue | fix acquisition if possible, interpolate/reject/correct |
| Normal variant / benign pattern | Real physiological EEG but not target | state-linked morphology, recurrence, lack of pathologic evolution | preserve or annotate, do not over-clean |

## Physiological Artifacts

### Eye Blink

- Waveform: large slow transient, often triangular or rounded, frequently 100-300 ms but variable; may dwarf ERP components.
- Distribution: maximal at Fp1/Fp2/AF/F sites with steep posterior falloff; usually bilateral for vertical blink.
- Frequency: mainly delta/theta with broad low-frequency power.
- Confounds: frontal P3a, slow cortical potential, P300 if blinks are time-locked to rare targets.
- Verification: EOG channel, frontal topomap, blink annotations/video, ICA eye component, target-vs-standard blink rate.
- Handling: ICA/SSP/regression/epoch rejection; avoid deleting all target trials if blinks are condition-biased.

### Vertical And Lateral Eye Movement / Saccade

- Waveform: step-like or slow deflection for gaze shift; saccades can add spike-like extraocular EMG.
- Distribution: vertical movements affect frontopolar channels; lateral movements oppose F7/F8 or left/right frontal polarity.
- Confounds: frontal slow waves, lateralized temporal activity, response-locked components.
- Verification: horizontal/vertical EOG, gaze logs, task display layout, polarity reversal across lateral frontal electrodes.

### EMG: Jaw, Temporalis, Forehead, Neck

- Waveform: irregular spiky bursts, short-duration potentials, often dense high-frequency activity.
- Distribution: temporal/frontal/neck-proximal electrodes; can spread widely in low-density montages.
- Frequency: broadband high frequency, often 20-100+ Hz; jaw clench can contaminate beta/gamma.
- Confounds: gamma-band neural activity, beta rebound, sleep muscle tone, movement-related potentials.
- Verification: PSD high-frequency slope, EMG channels, video, instructions to relax jaw, ICA muscle class, burst timing with speech/chewing/swallowing.
- Handling: prevent by task instruction, reject burst epochs, ICA/ASR if preserving continuous data; do not overinterpret gamma without EMG checks.

### Tongue, Swallowing, Chewing, Speech

- Waveform: broad slow fields plus EMG bursts; tongue dipole can create frontal-to-occipital gradients.
- Distribution: inferior/frontal/temporal emphasis; may appear widespread.
- Frequency: variable; tongue movement can appear in delta; chewing adds rhythmic EMG.
- Verification: audio/video, task logs, oral movement instruction, ICA, EMG.

### ECG And Cardiac Artifact

- Waveform: sharp or pulse-like recurring complexes time-locked to QRS, sometimes followed by delayed pulse artifact.
- Distribution: montage/reference-dependent; often visible in referential montages or near mastoids/ears.
- Frequency: heart-rate periodicity, commonly around 1 Hz plus waveform harmonics.
- Confounds: epileptiform-looking sharp waves, low-frequency rhythm, pulse-related electrode motion.
- Verification: ECG channel, pulse oximeter, constant R-R timing, delay of pulse artifact after QRS.
- Handling: ICA/SSP/regression if needed; include ECG channel in acquisition when possible.

### Pulse Artifact

- Waveform: slow wave or small transient linked to vascular pulsation near an electrode; delayed after ECG QRS.
- Distribution: often local to electrode over pulsating vessel.
- Verification: ECG/pulse timing, electrode location, pulse sensor, montage comparison.

### Respiration

- Waveform: slow rhythmic baseline movement or electrode-pressure artifact; sometimes sharp at inhalation/exhalation.
- Distribution: channels affected by body/head movement or lying pressure.
- Frequency: respiration-rate periodicity.
- Verification: respiration belt, video, technologist notes, coherence with breathing cycle.

### Sweat / Galvanic Skin Response

- Waveform: very slow baseline drift/sway, often huge low-frequency fluctuation.
- Distribution: can be broad but may depend on electrode gel/skin impedance.
- Frequency: ultra-low/delta drift; worsens with heat, stress, long sessions.
- Verification: impedance, session temperature, skin drying, low-frequency trend, simultaneous autonomic measures.
- Handling: improve acquisition, dry scalp, high-pass only if compatible with analysis; avoid distorting slow cortical potentials.

### Head And Body Movement

- Waveform: nonstationary bursts, baseline shifts, electrode-motion transients, cable sway, low-frequency movement plus broadband bursts.
- Distribution: variable; can be local or widespread.
- Verification: accelerometer/IMU, video, task timing, cable logs, electrode contact.
- Handling: annotate movement periods, ASR for transient high-amplitude bursts if appropriate, reject severe segments, redesign task if movement is systematic.

## External And Instrumental Noise

### 50/60 Hz Line Noise And Harmonics

- Waveform: near-sinusoidal narrowband activity; may be visible in raw traces if strong.
- Distribution: often broad; worse in high-impedance or poorly grounded channels.
- Frequency: exact power-line frequency and harmonics; frequency can drift slightly.
- Confounds: SSVEP stimulus frequency/harmonics, high-frequency brain/EMG analysis.
- Verification: PSD narrow peak, compare to stimulus frequencies, inspect harmonics, check mains frequency and recording environment.
- Handling: CleanLine/multitaper regression or narrow notch as appropriate; avoid notching away target SSVEP bins.

### Electrode Pop

- Waveform: abrupt vertical transient, step, or sharp waveform from sudden impedance change; often does not physiologically propagate.
- Distribution: usually one electrode or channels sharing one electrode in bipolar montage.
- Confounds: spikes/sharp waves, ERP transients.
- Verification: montage comparison, impedance, single-electrode localization, no consistent physiological field.
- Handling: mark segment/channel; interpolate if channel is repeatedly unstable.

### High Impedance / Poor Contact

- Waveform: noisy, drifting, high variance, intermittent pops, or low SNR.
- Distribution: one or a few channels; may contaminate reference if reference electrode is bad.
- Verification: impedance, channel variance, correlation/predictability, robust z-score, reference comparison.
- Handling: fix electrode during acquisition; after acquisition mark bad channels and interpolate if sufficient neighbors exist.

### Bridged Electrodes

- Waveform: two or more channels look nearly identical because gel/saline creates an electrical bridge.
- Distribution: local neighboring electrodes with unusually high correlation and reduced spatial detail.
- Verification: pairwise correlation, topographic implausibility, impedance/gel notes.
- Handling: mark bridged channels, avoid spatial analyses relying on independent electrodes.

### Bad / Flat / No-Data Channel

- Waveform: constant value, near-zero variance, NaN, dropout, random high noise, or impossible quantization.
- Distribution: isolated channel or device group.
- Verification: flatline duration, NaN count, low amplitude plus poor correlation, RANSAC predictability, channel quality report.
- Handling: exclude from ICA if severe; interpolate after robust reference if montage supports it.

### Dropout And Packet Loss

- Waveform: repeated samples, missing blocks, discontinuities, flat segments, timestamp gaps.
- Distribution: often all channels or wireless-device groups.
- Verification: sample counters, timestamps, xdf/log files, flatline/repeated-value detection.
- Handling: annotate discontinuities; do not treat as neural silence.

### Clipping / Saturation

- Waveform: plateau at amplifier limit; squared-off peaks; repeated maximum/minimum values.
- Distribution: channel-specific or amplifier-wide.
- Verification: hardware range, exact repeated extrema, histogram spikes at limits.
- Handling: reject saturated intervals; clipped signal cannot be reliably recovered.

### Reference Or Ground Failure

- Waveform: widespread common noise, sudden changes in many/all channels, impossible global artifacts.
- Distribution: broad, reference-dependent; may make many channels appear bad.
- Verification: compare references, inspect reference/ground electrode, ordinary vs robust average reference, common-mode changes.
- Handling: identify reference issue before removing many scalp channels; robust referencing may help after excluding unusable channels.

### Cable, USB, Bluetooth, And Environmental Interference

- Waveform: movement-linked bursts, periodic digital noise, dropouts, oscillatory interference.
- Distribution: cable/device-group-specific or broad.
- Verification: hardware logs, accelerometer, cable touch tests, unplug nearby devices, channel groups.
- Handling: acquisition redesign; annotate/drop contaminated segments.

### Trigger, Stimulus, Or Photodiode Leakage

- Waveform: precisely stimulus-locked electrical artifact, often too early, too sharp, or present in non-neural control channels.
- Distribution: can affect many channels through amplifier or cable coupling.
- Confounds: early evoked potentials, SSVEP, RSVP ERP.
- Verification: trigger lines, photodiode, blank trials, disconnected electrodes, latency too close to zero, polarity identical across channels.
- Handling: fix hardware isolation; model or exclude affected window if recovery is impossible.

## Not Artifacts But Easy To Misclassify

- Posterior alpha and alpha blocking: expected state-dependent rhythm.
- Central mu rhythm: can look arch-shaped or sharp; suppressed by movement/MI.
- Sleep spindles, K-complexes, vertex waves, POSTS: sleep-stage features, not noise.
- Lambda waves: posterior transients during visual scanning.
- Benign variants such as wicket rhythms, rhythmic temporal theta of drowsiness, small sharp spikes/BETS, 14-and-6-Hz positive spikes, and SREDA: require clinical context and expertise.
- Pathological EEG patterns: not "artifact" merely because they are high amplitude or sharp; do not diagnose, and recommend expert clinical review.
