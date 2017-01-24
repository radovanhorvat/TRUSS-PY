
(defun c:TP_draw_stresses ( / old_env_vars ins_pt force_data filename
						   xc yc counter data_line x1 y1 z1 x2 y2 z2 F pt1 pt2
						   dx dy ins_x ins_y text_x text_y pt_text text_str
						   ln_tension ln_compression ln_zero)

	(setq old_env_vars (env_get))
	(setvar "osmode" 0)
	(setvar "cmdecho" 0)

	(setq ln_tension "TRUSSPY_stress_T")
	(setq ln_compression "TRUSSPY_stress_C")
	(setq ln_zero "TRUSSPY_stress_Z")
	
	(command-s "._LAYER" "M" ln_tension "C" "140" "" "")
	(command-s "._LAYER" "M" ln_compression "C" "1" "" "")
	(command-s "._LAYER" "M" ln_zero "C" "7" "" "")
	
	(setq filename (strcat (getvar "dwgprefix") (getvar "dwgname")))
	(setq filename (vl-string-trim ".dwg" filename))
	(setq filename (strcat filename ".str"))	
	
	(setq force_data (read_csv filename))
	
	(setq ins_pt (getpoint "\nSpecify diagram insertion point: "))
	(setq ins_x (car ins_pt))
	(setq ins_y (cadr ins_pt))
	
	(setq counter 0)
	(repeat (length force_data)		
		(setq data_line (nth counter force_data))
		(if (= counter 0)
			(progn
				(setq xc (nth 0 data_line))
				(setq yc (nth 1 data_line))
				(setq dx (- ins_x xc))
				(setq dy (- ins_y yc))	
			)
			(progn
				(setq x1 (nth 0 data_line))				
				(setq y1 (nth 1 data_line))				
				(setq z1 (nth 2 data_line))
				(setq x2 (nth 3 data_line))
				(setq y2 (nth 4 data_line))				
				(setq z2 (nth 5 data_line))
				(setq F (nth 6 data_line))				

				(setq x1 (+ x1 dx))
				(setq y1 (+ y1 dy))
				(setq x2 (+ x2 dx))
				(setq y2 (+ y2 dy))
				
				(setq text_x (/ (+ x1 x2) 2))
				(setq text_y (/ (+ y1 y2) 2))			
			
				(setq pt1 (list x1 y1 z1))
				(setq pt2 (list x2 y2 z2))
				(setq pt_text (list text_x text_y 0))
				(setq text_str (rtos F 2 2))

				(if (> F 0)
					(setvar "CLAYER" ln_tension)
				)
				(if (< F 0)
					(setvar "CLAYER" ln_compression)
				)
				(if (= F 0)
					(setvar "CLAYER" ln_zero)
				)
				
				(command-s "._LINE" pt1 pt2 "")				
				(command-s "._TEXT" "J" "C" pt_text 0.1 0 text_str)				
			)
		)
		
		(setq counter (+ 1 counter))
	)
	
	
	(env_set old_env_vars)
	(princ)
)

