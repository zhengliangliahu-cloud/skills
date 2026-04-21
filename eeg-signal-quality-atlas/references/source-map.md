# Source Map

Research date: 2026-04-21

Use this file to cite the basis for the atlas or to extend it. Prefer primary literature, peer-reviewed reviews, and authoritative clinical references.

## Artifact And Noise Reviews

- Jiang, Bian, and Tian, "Removal of Artifacts from EEG Signals: A Review", Sensors 2019. URL: https://www.mdpi.com/1424-8220/19/5/987
  - Used for: intrinsic/extrinsic artifact framing, ocular/cardiac/external artifact categories, EEG band overview.
- Benbadis, "EEG Artifacts", Medscape, updated 2024. URL: https://emedicine.medscape.com/article/1140247-overview
  - Used for: practical morphology and distribution of muscle, tongue, eye, ECG, pulse, respiration, sweat, and non-physiologic artifacts.
- Sheng, Nalleballe, and Yadala, "EEG Benign Variants", NCBI Bookshelf/StatPearls, updated 2024. URL: https://www.ncbi.nlm.nih.gov/books/NBK555899/
  - Used for: normal rhythms, benign variants, and misclassification risk in clinical EEG.

## Paradigm Sources

- Shahid, Sinha, and Prasad, "Mu and beta rhythm modulations in motor imagery related post-stroke EEG", BMC Neuroscience 2010. URL: https://link.springer.com/article/10.1186/1471-2202-11-S1-P127
  - Used for: MI mu/beta ERD/ERS, C3/C4 sensorimotor focus, rehabilitation caveats.
- Polich, "Updating P300: An integrative theory of P3a and P3b", Clinical Neurophysiology 2007. DOI: https://doi.org/10.1016/j.clinph.2007.04.019
  - Used for: P3a/P3b conceptual distinction, amplitude/latency factors.
- "Predictive Power of Cognitive Biomarkers in Neurodegenerative Disease Drug Development: Utility of the P300 Event-Related Potential", PMC. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9666049/
  - Used for: P300 250-500 ms methodology, amplitude/latency, common electrode sites.
- Norcia et al., "The steady-state visual evoked potential in vision research: A review", Journal of Vision 2015. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC4581566/
  - Used for: SSVEP periodic response, frequency-domain interpretation, harmonics, phase.
- Li et al., "Brain-Computer Interface Speller Based on Steady-State Visual Evoked Potential", Brain Sciences 2021. URL: https://www.mdpi.com/2076-3425/11/4/450
  - Used for: SSVEP BCI framing, speller/stimulus paradigm context.
- Wang et al., "The Validity of Steady-State Visual Evoked Potentials as Attention Tags and Input Signals", Brain Sciences 2020. URL: https://www.mdpi.com/2076-3425/10/9/616
  - Used for: SSVEP as attention tag and BCI input.

## Physiological Artifact Characterization

- Kappel et al., "Physiological artifacts in scalp EEG and ear-EEG", BioMedical Engineering OnLine 2017. URL: https://link.springer.com/article/10.1186/s12938-017-0391-2
  - Used for: real-life/wearable EEG artifact concerns, jaw artifact, blink/eye movement SNR deterioration, ear-EEG caveats.

## Automated QC And Preprocessing

- Bigdely-Shamlo et al., "The PREP pipeline: standardized preprocessing for large-scale EEG analysis", Frontiers in Neuroinformatics 2015. URL: https://www.frontiersin.org/journals/neuroinformatics/articles/10.3389/fninf.2015.00016/full
  - Used for: line-noise removal, robust reference, bad-channel detection, deviation/correlation/predictability/HF-noise logic.
- Nolan, Whelan, and Reilly, "FASTER: Fully Automated Statistical Thresholding for EEG artifact Rejection", Journal of Neuroscience Methods 2010. URL: https://www.sciencedirect.com/science/article/pii/S0165027010003894
  - Used for: automated statistical artifact rejection, channel/epoch/component outlier features, ERP baseline variance.
- Jas et al., "Autoreject: Automated artifact rejection for MEG and EEG data", NeuroImage 2017. URL: https://www.sciencedirect.com/science/article/pii/S1053811917305013
  - Used for: cross-validated peak-to-peak thresholds, local bad-sensor repair, bad-trial decisions.
- Blum et al., "A Riemannian Modification of Artifact Subspace Reconstruction for EEG Artifact Handling", Frontiers in Human Neuroscience 2019. URL: https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2019.00141/full
  - Used for: ASR/rASR overview, online/offline multichannel artifact correction, mobile EEG context.
- Chang et al., "Evaluation of Artifact Subspace Reconstruction for Automatic Artifact Components Removal in Multi-Channel EEG Recordings", IEEE TBME 2020. DOI: https://doi.org/10.1109/TBME.2019.2930186
  - Used for: ASR parameter caution and actual EEG evaluation.
- Pion-Tonachini, Kreutz-Delgado, and Makeig, "The ICLabel dataset of electroencephalographic independent component features", Data in Brief 2019. URL: https://www.sciencedirect.com/science/article/pii/S235234091930455X
  - Used for: ICA component categories brain, muscle, eye, heart, line noise, channel noise, other; PSD/topography/autocorrelation feature basis.

## Maintenance Notes

- Add new sources when extending a paradigm or adding a tool-specific workflow.
- Record source date and why the source changes a rule.
- Keep detailed literature notes here, not in `SKILL.md`, so the skill entry stays lightweight.
