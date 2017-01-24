
(defun c:TP_draw_reactions ( / old_env_vars ins_pt force_data force_data2 filename1 filename2
						   xc yc counter data_line x1 y1 z1 x2 y2 z2 F pt1 pt2
						   dx dy ins_x ins_y text_x text_y pt_text text_str
						   ln_tension ln_compression ln_zero)

	; DRAW GRAPHICS FIRST
	(setq old_env_vars (env_get))
	(setvar "osmode" 0)
	(setvar "cmdecho" 0)

	(setq reactions_layer "TRUSSPY_reactions")
	(setq element_layer "TRUSSPY_elements")

	(command-s "._LAYER" "M" reactions_layer "C" "2" "" "")
	(command-s "._LAYER" "M" element_layer "C" "4" "" "")	
	
	(setq filename1 (strcat (getvar "dwgprefix") (getvar "dwgname")))
	(setq filename1 (vl-string-trim ".dwg" filename1))
	(setq filename1 (strcat filename1 ".gtr"))	

	(setq filename2 (vl-string-trim ".gtr" filename1))
	(setq filename2 (strcat filename2 ".rct"))
	
	(setq force_data (read_csv filename1))
	(setq force_data2 (read_csv filename2))
	
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
				;(setq node1_label (nth 2 data_line))	
				(setq x2 (nth 3 data_line))
				(setq y2 (nth 4 data_line))				
				;(setq node2_label (nth 5 data_line))
				;(setq element_label (nth 6 data_line))				

				(setq x1 (+ x1 dx))
				(setq y1 (+ y1 dy))
				(setq x2 (+ x2 dx))
				(setq y2 (+ y2 dy))
				
				;(setq text_x (/ (+ x1 x2) 2))
				;(setq text_y (/ (+ y1 y2) 2))			
			
				(setq pt1 (list x1 y1 0))
				(setq pt2 (list x2 y2 0))
				;(setq pt_text (list text_x text_y 0))
				;(setq text_str_el (strcat "el "(rtos element_label 2 0)))
				;(setq text_str_nd1 (strcat "nd " (rtos node1_label 2 0)))
				;(setq text_str_nd2 (strcat "nd " (rtos node2_label 2 0)))
				
				(setvar "CLAYER" element_layer)				
				(command-s "._LINE" pt1 pt2 "")				
				;(setvar "CLAYER" ln_element_labels)				
				;(command-s "._TEXT" "J" "C" pt_text 0.1 0 text_str_el)				
				;(setvar "CLAYER" ln_node_labels)				
				;(command-s "._TEXT" "J" "C" pt1 0.1 0 text_str_nd1)
				;(command-s "._TEXT" "J" "C" pt2 0.1 0 text_str_nd2)
			)
		)
		
		(setq counter (+ 1 counter))
	)

	; DRAW REACTIONS
	(setq counter 0)
	(repeat (length force_data2)		
		(setq data_line (nth counter force_data2))


		(setq x1 (nth 0 data_line))				
		(setq y1 (nth 1 data_line))				
		(setq prefix (nth 2 data_line))
		(setq R_x (nth 3 data_line))
		(setq R_y (nth 4 data_line))
		
		(setq x1 (+ x1 dx))
		(setq y1 (+ y1 dy))		

		(setq pt1 (list x1 y1 0))

		(setvar "CLAYER" reactions_layer)
		(if (= prefix 1)
			(progn
				(setq text_str_react (strcat "Rx: "(rtos R_x 2 2)))
				(command-s "._TEXT" "J" "L" pt1 0.1 0 text_str_react)
			)
		)
		(if (= prefix 2)
			(progn
				(setq text_str_react (strcat "Ry: "(rtos R_y 2 2)))
				(command-s "._TEXT" "J" "L" pt1 0.1 0 text_str_react)				
			)
		)		
		(if (= prefix 3)
			(progn
				(setq text_str_react1 (strcat "Rx: "(rtos R_x 2 2)))
				(setq text_str_react2 (strcat "Ry: "(rtos R_y 2 2)))
				(command-s "._TEXT" "J" "L" pt1 0.1 0 text_str_react1)
				(setq pt_down (list (car pt1) (- (cadr pt1) 0.15 ) (caddr pt1)))
				(command-s "._TEXT" "J" "L" pt_down 0.1 0 text_str_react2)
			)
		)
		
		
				
						
	
		
		(setq counter (+ 1 counter))
	)
	
	(env_set old_env_vars)
	(princ)
)

