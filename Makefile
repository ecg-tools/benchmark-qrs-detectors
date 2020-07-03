
.PHONY: detection correction evaluation clean help viz

evaluation: output/frames/${ALGO}_${DATASET}.json output/annotations/${DATASET}.json
	@python get_perf.py --data ${DATASET} --algo ${ALGO} --tol ${TOLERANCE}

detection output/frames/${ALGO}_${DATASET}.json:
	@python perform_detection.py --data ${DATASET} --algo ${ALGO}

correction output/annotations/${DATASET}.json:
	@python get_annotations.py --data ${DATASET}

viz:
	@python streamlit run dashboard.py

help:
	@echo DATASET : string - dataset to choose among this list ['mit-bih-arrhythmia', 'mit-bih-noise-stress-test-e24',
	@echo	  'mit-bih-noise-stress-test-e18', 'mit-bih-noise-stress-test-e12', 'mit-bih-noise-stress-test-e06',
	@echo	  'mit-bih-noise-stress-test-e00', 'mit-bih-noise-stress-test-e_6', 'european-stt',
	@echo	  'mit-bih-supraventricular-arrhythmia', 'mit-bih-long-term-ecg']
	@echo
	@echo ALGO : string - algorithm to choose among this list ['Pan-Tompkins-ecg-detector', 'Hamilton-ecg-detector',
	@echo	  'Christov-ecg-detector', 'Engelse-Zeelenberg-ecg-detector', 'SWT-ecg-detector',
	@echo	  'Matched-filter-ecg-detector', 'Two-average-ecg-detector', 'Hamilton-biosppy', 'Christov-biosppy',
	@echo	  'Engelse-Zeelenberg-biosppy', 'Gamboa-biosppy', 'mne-ecg', 'heartpy', 'gqrs-wfdb', 'xqrs-wfdb']
	@echo
	@echo TOLERANCE : int - tolerance of the evaluation in millisecond

clean:
	rm -f output/*


