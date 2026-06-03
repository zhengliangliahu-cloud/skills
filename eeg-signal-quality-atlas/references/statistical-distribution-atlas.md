# Statistical Distribution Atlas

Use this reference only for statistical distributions of EEG values and features. Do not use it as a scalp topography or electrode-localization guide. Here, "distribution" means how raw samples, window features, spectral values, trial features, channel-quality scores, or ICA-component features are distributed across time, windows, epochs, channels, trials, subjects, or conditions.

## Core Principle

Clean EEG is not expected to be perfectly normal/Gaussian. Treat clean EEG as data whose statistics are physiologically plausible, condition-consistent, and relatively stable after accounting for state, paradigm, reference, and preprocessing. Artifacts and noise are often detected because they distort feature distributions: heavy tails, extreme outliers, multimodal mixtures, degenerate values, boundary piles, narrow spectral spikes, broadband high-frequency tails, or condition-biased missing/rejected trials.

## Summary Table

| Source class | Raw amplitude distribution | Window/epoch feature distribution | Frequency-domain distribution | Trial/event distribution | Component/channel distribution |
| --- | --- | --- | --- | --- | --- |
| Clean neural EEG | Continuous values with finite variance; state- and rhythm-dependent deviations from normality are expected | Variance, entropy, kurtosis, and peak-to-peak are stable relative to task state and neighboring data | Band-limited physiological peaks or task-related spectral changes | Effects align with task labels, baseline, and expected latency/frequency | Brain ICs and good channels have plausible spectra, autocorrelation, and non-outlier quality metrics |
| Physiological artifact | Heavy tails, bursts, slow drifts, or repeated large transients depending on source | Elevated peak-to-peak, variance, kurtosis, HF-noise ratio, baseline drift, or condition-biased outlier rate | Ocular low-frequency power, EMG broadband high-frequency tail, ECG periodic harmonics | May be locked to behavior, fatigue, response, or stimulus in a biased way | Eye/muscle/heart ICs form distinctive outlier groups in PSD, autocorrelation, and time-course features |
| External/instrumental noise | Degenerate, discontinuous, clipped, repeated, or implausibly random values | Robust z-score outliers, low entropy, zero/near-zero variance, excessive line-noise ratio, poor predictability | Narrow mains-frequency peaks, device-specific periodic noise, or broadband random noise | Usually not physiologically task-specific; may align with hardware events or dropouts | Bad channels and channel-noise ICs are outliers in variance, correlation, predictability, and spectral measures |

## Raw Amplitude Distribution

### Clean EEG

- Clean EEG raw samples are usually continuous and bounded by physiological and amplifier constraints, but they are not required to be Gaussian.
- Mild skewness, nonstationarity, and band-limited oscillatory structure are normal when state changes, alpha/mu rhythms, sleep features, slow potentials, or evoked responses are present.
- Across short stationary windows, amplitude spread should be reasonably stable relative to nearby windows from the same state and reference.
- Clean task effects should change distributions in a paradigm-consistent way, such as ERP mean shifts after event averaging or bandpower shifts during MI.

### Blink, saccade, and ocular artifact

- Blinks create heavy tails and large peak-to-peak outliers in raw amplitude windows.
- If blinks occur more often in one condition, the target/standard or class-specific amplitude distribution can become biased.
- Slow eye movement creates step-like or low-frequency shifts that broaden amplitude distributions and inflate baseline drift.
- A single amplitude threshold can misclassify ocular-contaminated target trials as neural P300 unless condition-specific blink rates are checked.

### EMG and movement artifact

- EMG creates bursty raw-value distributions: high kurtosis within burst windows and heavy tails relative to quiet baseline.
- Movement can create mixed distributions: slow shifts plus broadband bursts, often producing nonstationary variance across adjacent windows.
- Speech, chewing, swallowing, and jaw tension can create repeated burst clusters rather than isolated outliers.

### Electrode pop, dropout, flatline, and clipping

- Electrode pop creates abrupt extreme samples or step changes, often producing very high kurtosis in a short window.
- Flatline produces degenerate amplitude distribution: near-zero variance and low entropy.
- Dropout can create repeated values, timestamp gaps, or block-level discontinuities; the value distribution may show unnatural spikes at repeated samples.
- Clipping creates boundary piles at amplifier maximum/minimum values and flattened tails; clipped data should not be treated as recoverable neural amplitude.

## Window And Epoch Feature Distribution

Compute features over fixed windows or epochs, then compare the feature distribution against robust within-recording baselines. Use median, IQR, median absolute deviation, percentile intervals, and robust z-score before relying on mean and standard deviation.

| Feature | Clean EEG pattern | Artifact/noise pattern | Main caveat |
| --- | --- | --- | --- |
| peak-to-peak | Stable within state; ERP epochs may differ after stimulus | High outliers for blink, pop, movement, EMG burst | High-amplitude sleep or slow potentials can be clean |
| variance / robust variance | State- and channel-dependent but not isolated extreme | High for noisy channels/EMG/movement; low for flatline | Reference changes alter variance |
| kurtosis | Moderate deviations possible from oscillations/ERPs | High for pops, bursts, spikes, clipping edges | Rare neural transients can also increase kurtosis |
| skewness | Can shift with slow potentials or baseline | Large sign-dependent shifts from drift, clipping, steps | Reference and high-pass choices matter |
| entropy | Physiological complexity but not random white noise | Low in flatline/dropout; abnormal in random channel noise | Entropy depends strongly on estimator and filtering |
| baseline drift | Stable after appropriate baseline correction | Large slow changes from sweat, electrode drift, respiration | Do not erase valid slow cortical potentials |
| HF-noise ratio | Low to moderate unless task targets high frequency | High for EMG and high-frequency channel noise | Gamma studies need stronger controls |
| line-noise ratio | Low or stable after line-noise correction | High narrow mains peaks or harmonics | SSVEP target bins can overlap mains harmonics |
| robust z-score | Most windows close to baseline | Artifact windows and bad channels are outliers | Z-scores need comparable windows and channels |

## Frequency-Domain Distribution

### Clean rhythms and task signals

- Clean resting rhythms often concentrate power in physiological bands, such as alpha, mu, beta, theta, or sleep-specific bands.
- MI changes are usually observed as class/time-dependent distributions of mu/beta bandpower or ERD/ERS values, not as one universal amplitude distribution.
- P300 is primarily an event-related time-domain effect; frequency distributions are useful for baseline/noise checks, not for replacing ERP amplitude/latency evidence.
- SSVEP concentrates energy at stimulus frequency and harmonics, and the distribution of spectral power should change with attended target frequency.

### EMG

- EMG tends to add a broadband high-frequency tail, often increasing power across beta/gamma and above.
- EMG-contaminated windows should be outliers in HF-noise ratio, high-frequency bandpower, and sometimes kurtosis.
- A narrow peak alone is not typical EMG evidence; check for broadband elevation.

### Line noise

- Line noise produces extremely narrow concentration at mains frequency, usually 50 Hz or 60 Hz, and possible harmonics.
- Its distribution is usually unrelated to task labels, except when hardware or stimulus timing accidentally couples to the task.
- If an SSVEP target frequency or harmonic overlaps mains frequency, separate evidence by task dependence: SSVEP follows target/stimulus bins; line noise follows mains bins across conditions.

### Bad channel and random noise

- Bad channels may show excessive broadband power, unstable spectral shape, or spectral distributions unlike other channels.
- Random channel noise may increase entropy and reduce autocorrelation while producing poor correlation/predictability with neighboring channels.

## Trial And Event Distribution

### P300 vs blink

- P300 evidence should appear as target/standard distribution differences in amplitude and latency, commonly in a 250-500 ms analysis window, after baseline correction.
- Single-trial P300 amplitude/latency can vary, but averaged target trials should show a coherent central tendency relative to standards.
- Blink contamination produces heavy-tailed peak-to-peak and amplitude distributions, often with extreme trials that can dominate averages.
- If target trials contain more blinks than standard trials, an apparent P300 difference can be condition-biased. Compare rejection rate, blink rate, baseline variance, and EOG-linked features by condition.

### MI vs EMG

- MI should produce task-related distributions of mu/beta bandpower, ERD/ERS, covariance, or classifier features across imagery classes or time windows.
- EMG should produce burst/outlier distributions in high-frequency power, HF-noise ratio, kurtosis, and peak-to-peak.
- A useful check is whether class separation remains in mu/beta features after removing high-HF outlier windows.

### SSVEP vs line noise

- SSVEP should show energy concentration at stimulus frequency and harmonics, with spectral features distributed according to attended target labels.
- Line noise should show mains-frequency concentration largely independent of target labels, subject state, or stimulus frequency allocation.
- Compare feature distributions at stimulus bins, neighboring bins, and mains bins.

### Condition-biased artifact

- Artifacts can become predictive if they are unevenly distributed across conditions.
- Always compare artifact-rate distributions by condition/class: blink count, rejected epoch rate, peak-to-peak outlier rate, HF-noise outlier rate, and missing/dropout rate.
- A model can perform well by learning artifact distributions; check whether feature importance or class separation depends on artifact features.

## Channel And Component Feature Distribution

### Good channel vs bad channel

- Good channels should not be persistent outliers in robust variance, entropy, line-noise ratio, HF-noise ratio, flatline duration, dropout count, or predictability.
- Bad channels often form distribution outliers across channels: extreme robust z-score, low correlation, poor RANSAC predictability, excessive line noise, or near-zero variance.
- Flat channels are low-variance and low-entropy outliers; noisy channels are high-variance or high-HF outliers; bridged channels can show abnormally high pairwise correlation.

### ICA and ICLabel-style component distributions

- Brain IC: plausible PSD structure, autocorrelation, dipolar/source-like behavior, and task-related feature changes.
- Eye IC: low-frequency-dominant activity, blink/saccade time-course outliers, and high event-related amplitude in ocular windows.
- Muscle IC: broadband high-frequency distribution and bursty high-kurtosis windows.
- Heart IC: periodic autocorrelation and ECG-locked feature distribution.
- Line-noise IC: narrowband peak distribution at mains frequency/harmonics.
- Channel-noise IC: abnormal variance, low predictability, poor autocorrelation structure, or channel-specific noise concentration.
- Other IC: mixed or low-confidence distribution; preserve uncertainty rather than forcing a class.

## Clean EEG vs Noisy EEG

Do not define clean EEG as "normal distribution". Define it by a bundle:

- Feature distributions are stable within comparable states and windows.
- Outlier rates are low or explainable by task/state.
- Spectral features match physiological rhythms or paradigm targets.
- Trial/event feature differences match expected labels and timing.
- Bad-channel metrics are not persistent outliers.
- ICA/component distributions do not show dominant eye, muscle, heart, line-noise, or channel-noise evidence in the target signal.

Noisy EEG is suggested when:

- Multiple feature distributions become outlier-heavy or unstable.
- Missing, clipped, repeated, or flat values appear.
- Spectral power is dominated by mains peaks, broadband device noise, or EMG tails.
- Condition differences can be explained by artifact-rate distributions.
- Robust z-score, entropy, variance, and predictability disagree with physiological expectations.

## Reporting Template

Use this template when the user asks for distribution differences:

```text
统计分布判定:
- Raw amplitude distribution:
- Window/epoch feature distribution:
- Frequency-domain distribution:
- Trial/event distribution:
- Channel/component feature distribution:
- 主要混淆:
- 建议验证:
- 处理建议:
```

For tables, use:

`对象 | 纯净 EEG 的统计分布 | 伪迹/噪声的统计分布 | 关键特征 | 误判风险 | 验证动作`
