
(defun c:TP_draw_reactions ( / old_env_vars ins_pt geometry_data reaction_data filename1 filename2
						   xc yc counter data_line x1 y1 z1 x2 y2 z2 F pt1 pt2
						   dx dy ins_x ins_y text_x text_y pt_text text_str
						   ln_tension ln_compression ln_zero ln_reactions ln_element prefix
						   text_str_react text_str_react1 text_str_react2 pt_down)

	; DRAW GEOMETRY
	(setq old_env_vars (env_get))
	(setvar "osmode" 0)
	(setvar "cmdecho" 0)

	(setq ln_reactions "TRUSSPY_reactions")
	(setq ln_element "TRUSSPY_elements")

	(command-s "._LAYER" "M" ln_reactions "C" "2" "" "")
	(command-s "._LAYER" "M" ln_element "C" "4" "" "")	
	
	(setq filename1 (strcat (getvar "dwgprefix") (getvar "dwgname")))
	(setq filename1 (vl-string-trim ".dwg" filename1))
	(setq filename1 (strcat filename1 ".gtr"))	

	(setq filename2 (vl-string-trim ".gtr" filename1))
	(setq filename2 (strcat filename2 ".rct"))
	
	(setq geometry_data (read_csv filename1))
	(setq reaction_data (read_csv filename2))
	
	(setq ins_pt (getpoint "\nSpecify diagram insertion point: "))
	(setq ins_x (car ins_pt))
	(setq ins_y (cadr ins_pt))
	
	(setq counter 0)
	(repeat (length geometry_data)		
		(setq data_line (nth counter geometry_data))
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
				(setq x2 (nth 3 data_line))
				(setq y2 (nth 4 data_line))					

				(setq x1 (+ x1 dx))
				(setq y1 (+ y1 dy))
				(setq x2 (+ x2 dx))
				(setq y2 (+ y2 dy))				
		
				(setq pt1 (list x1 y1 0))
				(setq pt2 (list x2 y2 0))
			
				(setvar "CLAYER" ln_element)				
				(command-s "._LINE" pt1 pt2 "")				
			)
		)
		
		(setq counter (+ 1 counter))
	)

	; DRAW REACTIONS
	(setq counter 0)
	(repeat (length reaction_data)		
		(setq data_line (nth counter reaction_data))
		(setq x1 (nth 0 data_line))				
		(setq y1 (nth 1 data_line))				
		(setq prefix (nth 2 data_line))
		(setq R_x (nth 3 data_line))
		(setq R_y (nth 4 data_line))
		
		(setq x1 (+ x1 dx))
		(setq y1 (+ y1 dy))		

		(setq pt1 (list x1 y1 0))

		(setvar "CLAYER" ln_reactions)
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

