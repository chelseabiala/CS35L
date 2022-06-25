(defun which-line ()
  (interactive)
  (let((start (point-min))
       (n (line-number-at-pos))
       (l (count-matches "
" 1)))
    (if (= start 1)
	(message "Line %d of %d" n l)
      (save-excursion
	(save-restriction
	  (widen)
	  (message "line %d (narrowed line %d)"
		   (+ n (line-number-at-pos start) -1) n))))))
