# Paradigm Atlas

Use this reference to anchor artifact/noise decisions in the expected neural signature for the paradigm. A feature that is suspicious in one paradigm can be the target signal in another.

## Quick Coverage Matrix

| Paradigm | Clean signal to preserve | Main channels | Main time/frequency evidence | Frequent confounds |
| --- | --- | --- | --- | --- |
| Resting/spontaneous EEG | alpha, mu, beta, theta/delta by state | O/P for alpha, C for mu, broad scalp | state-dependent rhythms, symmetry, reactivity | drowsiness, blinks, EMG, sweat drift, line noise |
| Clinical/sleep EEG | sleep spindles, K-complexes, vertex waves, POSTs, normal rhythms/variants | state-specific | stage-linked morphology and recurrence | muscle, eye movement, ECG, benign variants overcalled as pathology |
| MI/SMR | mu/beta ERD/ERS during imagery | C3/C4/Cz, sensorimotor cortex | 8-13 Hz mu, 13-30 Hz beta, lateralized ERD/ERS | jaw EMG, movement, attention alpha, bad C electrodes |
| P300/oddball ERP | positive ERP around 250-500 ms, often parietal/central | Pz, Cz, CP/P sites | target vs standard difference, latency/amplitude | blink, slow drift, trigger error, motor response |
| SSVEP/SSMVEP | frequency-locked response and harmonics | O1/O2/Oz, PO/P sites | stimulus frequency, phase stability, harmonics | 50/60 Hz line noise, monitor refresh artifacts, eye fatigue |
| VEP/AEP/SEP | modality-specific evoked components | O for VEP, temporal/central for AEP, somatosensory sites for SEP | stimulus-locked averaged response | sensory artifact, startle EMG, trigger latency |
| ErrP/ERN/FRN | response/error/feedback-locked negativity | FCz/Cz/frontocentral | response or feedback locked, tens to hundreds ms | muscle from button press, ocular correction, feedback visual ERP |
| RSVP | rapid visual ERP components, target P300/N2 | posterior/parietal | precise stimulus stream timing | overlap, blink suppression/rebound, trigger jitter |
| Emotion/affective EEG | alpha asymmetry, late positive potential, bandpower changes | frontal, central, parietal | condition effects, trial/block stability | facial EMG, autonomic sweat, movement, stimulus leakage |
| Attention/workload | theta/alpha/beta changes, ERP modulation | frontal midline, parietal/occipital | task load relation, baseline-corrected features | fatigue, eye movements, muscle tension |
| Neurofeedback | trained rhythm modulation | target-specific | gradual controllable change, feedback timing | reward/feedback artifact, motion, learning drift |
| Mobile/wearable EEG | same neural targets under lower SNR | device-dependent | artifact-aware repeated evidence | movement, cable/electrode motion, wireless dropouts |
| Hybrid BCI | combined MI/P300/SSVEP/etc. | combined | each component must match its own timing/topography | feature leakage, overlapping artifact, incorrect labels |

## Resting And Spontaneous EEG

Clean signals:

- Posterior dominant alpha: usually 8-13 Hz, strongest over occipital/parietal areas, increases with eyes closed, attenuates with eyes open or attention.
- Mu rhythm: 8-13 Hz over central sensorimotor areas, arch-shaped in raw traces, suppressed by movement, motor imagery, or action observation.
- Beta: 13-30 Hz, often frontocentral/sensorimotor, affected by alertness, medication, and muscle contamination.
- Theta/delta: state-dependent; expected in drowsiness/sleep, suspicious if focal or unexpected in awake adult research data.

Most common artifacts/noise:

- Eye blinks and slow eye movements during eyes-open/closed transitions.
- EMG from jaw, forehead, neck tension, especially in beta/gamma ranges.
- Sweat/GSR drift during long resting blocks.
- Line noise and reference/ground problems in low-density or wearable systems.

Recommended features:

- PSD and bandpower by state; alpha reactivity; channel symmetry; frontal EOG correlation; HF-noise ratio; line-noise ratio; robust channel variance.

## Clinical And Sleep EEG

Clean signals:

- Sleep features: vertex waves, K-complexes, sleep spindles, POSTS, slow waves, REM-related eye movements, depending on sleep stage.
- Normal rhythms and benign variants can be sharply contoured or rhythmic and still nonpathological; context, state, recurrence, and lack of evolution are essential.
- Physiological state markers such as eye movements or muscle tone may be useful for staging even when they are artifacts for cognitive ERP analysis.

Most common artifacts/noise:

- Muscle artifacts from jaw/tongue/swallowing, ECG/pulse, respiration, sweat, electrode pops, and movement.
- Benign variants or normal rhythms misread as abnormal activity.

Recommended features:

- State annotation, montage comparison, recurrence, evolution, background disruption, video/ECG/respiration channels, and expert review for clinical claims.

## Motor Imagery And SMR BCI

Clean signals:

- MI/SMR relies on event-related desynchronization/synchronization in mu and beta bands.
- Left/right hand MI often shows contralateral mu/beta ERD over C3/C4, with possible ipsilateral ERS or beta rebound after movement/imagery.
- Foot/tongue imagery can shift spatial patterns toward Cz or lateral sensorimotor representations.
- Signal may be delayed or weak in rehabilitation and post-stroke settings; do not require an immediate response in every subject.

Most common artifacts/noise:

- Actual muscle movement, jaw clench, shoulder/neck EMG, electrode motion near central electrodes, attention-related posterior alpha, and session drift.

Recommended features:

- Time-frequency ERD/ERS relative to baseline, CSP/Riemannian covariance, lateralization index, channel topomaps, trial-by-trial consistency, EMG/HF power checks, accelerometer or video if available.

## P300 And Oddball ERP

Clean signals:

- P300/P3 is a positive ERP elicited by rare, task-relevant, surprising, or target stimuli, typically measured by averaging time-locked epochs.
- Common latency window is roughly 250-500 ms after stimulus onset in many adult oddball tasks; latency shifts with task difficulty, age, modality, and pathology.
- P3b is often largest over parietal midline sites such as Pz; P3a can be more frontocentral.
- Key evidence is target-vs-standard difference, not a single large positive deflection in raw data.

Most common artifacts/noise:

- Blinks in the same post-stimulus window, slow baseline drift, response-related motor potentials, trigger jitter, stimulus leakage, and unbalanced trial rejection.

Recommended features:

- ERP amplitude/latency, target-standard difference wave, baseline variance, EOG channels, single-trial latency variance, percentage of rejected trials, event timing audit.

## SSVEP And SSMVEP

Clean signals:

- SSVEP is a periodic visual evoked response frequency-locked to repetitive stimulation; responses appear at the stimulus frequency and often harmonics.
- It is strongest over occipital and occipito-parietal electrodes and can have stable phase across time.
- SSMVEP/motion variants follow the motion reversal or oscillation frequency and related harmonics.

Most common artifacts/noise:

- Power-line peaks at 50/60 Hz and harmonics; display refresh/flicker artifacts; eye fatigue/blinks; head motion; stimulus frequencies that overlap line noise or another target's harmonic.

Recommended features:

- PSD narrowband peaks, SNR around stimulus bins, phase locking, canonical correlation analysis references, harmonic map, frequency allocation audit.

## VEP, AEP, And SEP

Clean signals:

- VEP: stimulus-locked occipital components after visual events; pattern reversal and flash VEP differ in latency and morphology.
- AEP: auditory components over frontocentral/temporal scalp; early sensory components and later cognitive components may overlap.
- SEP: somatosensory responses localized according to stimulated body part and pathway.

Most common artifacts/noise:

- Startle EMG, stimulus hardware artifacts, trigger delay, eye movements to visual stimuli, cable movement from tactile stimulation.

Recommended features:

- Averaged event response, replicate runs, latency consistency, modality-appropriate channels, trigger validation, control channels near stimulus hardware.

## ErrP, ERN, FRN, And Feedback Paradigms

Clean signals:

- ERN/Ne: response-locked frontocentral negativity after erroneous responses, often followed by Pe positivity.
- FRN: feedback-locked frontocentral negativity to unfavorable or unexpected feedback.
- ErrP: error-related potential when the system or user detects an error; timing depends on feedback/event.

Most common artifacts/noise:

- Button-press EMG, response movement, blink after error, feedback visual ERP, timing labels that mix response-locked and stimulus-locked events.

Recommended features:

- Response-locked vs feedback-locked averaging, FCz/Cz topography, correct-vs-error difference, EMG channels, reaction-time stratification.

## RSVP And Rapid Visual Streams

Clean signals:

- Target detection can yield N2/P3-family components, often posterior/parietal, but adjacent stimuli overlap in time.
- Clean effects should align with the exact item position and survive overlap-aware averaging or deconvolution.

Most common artifacts/noise:

- Trigger jitter, monitor timing error, blink suppression followed by rebound blinks, eye movements to salient targets.

Recommended features:

- Event timing audit, deconvolution/regression ERP, target/distractor contrast, blink distribution over stream position, response timing.

## Emotion And Affective EEG

Clean signals:

- Frontal alpha asymmetry, condition-related bandpower changes, late positive potential, and connectivity/covariance changes may be relevant depending on protocol.
- Effects are often block-level and vulnerable to subject state and peripheral physiology.

Most common artifacts/noise:

- Facial EMG from expression, jaw/forehead tension, autonomic sweat drift, heart/respiration changes, movement during naturalistic stimuli.

Recommended features:

- Condition-balanced PSD, facial EMG indicators, EOG/ECG/respiration controls, block drift checks, robust subject-level statistics.

## Attention, Vigilance, And Workload

Clean signals:

- Frontal midline theta, alpha suppression, posterior alpha modulation, beta changes, and ERP amplitude/latency shifts can all be target signals.
- Vigilance studies may intentionally track drowsiness; do not remove drowsiness patterns if they are the label.

Most common artifacts/noise:

- Eye closure, blink rate changes, posture/movement, fatigue-related muscle relaxation or tension, task interaction artifacts.

Recommended features:

- Baseline-corrected bandpower, blink metrics, state annotation, task-performance correlation, time-on-task trends.

## Neurofeedback

Clean signals:

- The target rhythm should change with feedback learning and show plausible topography for the trained feature.
- Feedback-loop timing can produce strong stimulus-locked effects that are not spontaneous rhythm control.

Most common artifacts/noise:

- Participant learns to change EMG, blink rate, respiration, or posture to manipulate feedback.

Recommended features:

- Control features outside the target band, EMG/EOG checks, sham/control blocks, transfer blocks without feedback, artifact-aware reward auditing.

## Mobile And Wearable EEG

Clean signals:

- Same neural phenomena as lab EEG can be present, but spatial resolution and SNR are lower and artifacts are more frequent.
- Ear-EEG and low-density systems can capture useful steady-state or alpha modulation while having device-specific artifact sensitivity.

Most common artifacts/noise:

- Electrode motion, cable motion, jaw artifacts in ear-EEG, wireless dropouts, impedance drift, accelerometer-linked bursts, environmental line noise.

Recommended features:

- Accelerometer correlation, dropout/flatline detection, robust z-scores over short windows, ASR suitability check, channel predictability, repeated-condition evidence.

## Hybrid BCI

Clean signals:

- Treat each sub-paradigm independently before fusing decisions: MI should match sensorimotor ERD/ERS, P300 should be event-locked ERP, SSVEP should be frequency-locked occipital response.

Most common artifacts/noise:

- A feature from one paradigm can masquerade as another, such as visual flicker harmonics affecting ERP baselines or motor response EMG contaminating ErrP/P300 windows.

Recommended features:

- Separate timing windows, separate spatial priors, leakage checks between labels, ablation by feature family, paradigm-specific artifact reports.
