(load "f_functions")
(vl-load-com)

(defun c:TP_export_model( / selection counter entitydata entname layer_name pt_start pt_end E A
							x1 y1 x2 y2 element_list support_list data_bin ins_pt f filename
							element_data support_data support_type support_string my_command)


	(setq element_list (list))
	(setq support_list (list))
	(setq filename (strcat (getvar "dwgprefix") (getvar "dwgname")))
	(setq filename (vl-string-trim ".dwg" filename))
	(setq filename (strcat filename ".tpy"))
	
	(setq selection (ssget '((-4 . "<or")							
							(0 . "LINE")(8 . "TRUSSPY_elements")
							(-4 . "<and")
							(8 . "TRUSSPY_supports")
							(-4 . "and>")
							(-4 . "or>")
							)
					)
	)
	
	(setq counter 0)
	(repeat (sslength selection)
		(setq entitydata (entget (ssname selection counter)))
		(setq entname (ssname selection counter))
		
		(setq layer_name (cdr (assoc 8 (entget entname))))
		
		(if (= layer_name "TRUSSPY_elements")
			(progn
				(setq pt_start (cdr (assoc 10 entitydata)))
				(setq pt_end (cdr (assoc 11 entitydata)))
				(setq E (vlax-ldata-get entname "E"))
				(setq A (vlax-ldata-get entname "A"))
				(setq x1 (car pt_start))
				(setq y1 (cadr pt_start))
				(setq x2 (car pt_end))
				(setq y2 (cadr pt_end))
				(setq data_bin (list x1 y1 x2 y2 E A))
				(setq element_list (cons data_bin element_list))
			)
		)

		(if (= layer_name "TRUSSPY_supports")
			(progn
				(setq ins_pt (cdr (assoc 10 entitydata)))
				(setq support_type (vlax-ldata-get entname "type"))
				(setq x1 (car ins_pt))
				(setq y1 (cadr ins_pt))
				(setq data_bin (list x1 y1 support_type))
				(setq support_list (cons data_bin support_list))
			)
		)
		
		(setq counter (+ 1 counter))
			
	 )	


	;(setq filename "E:/Python_Scripts/dsm3_output/output_file.txt")
	(setq f (open filename "w"))
	
	; write elements
	(setq counter 0)
	(write-line "ELEMENTS" f)
	(repeat (length element_list)
		(setq element_data (nth counter element_list))
		(setq x1 (nth 0 element_data))
		(setq y1 (nth 1 element_data))
		(setq x2 (nth 2 element_data))
		(setq y2 (nth 3 element_data))
		(setq E (nth 4 element_data))
		(setq A (nth 5 element_data))
		
		(write-line (strcat (rtos x1) "," (rtos y1) "," (rtos x2) "," (rtos y2) "," (rtos E) "," (rtos A)) f)
		
		(setq counter (+ 1 counter))
	)	
	(write-line "END ELEMENTS" f)
	(write-line "" f)
	
	; write supports
	(setq counter 0)
	(write-line "SUPPORTS" f)
	(repeat (length support_list)
		(setq support_data (nth counter support_list))
		(setq x1 (nth 0 support_data))
		(setq y1 (nth 1 support_data))
		(setq support_type (nth 2 support_data))		
		(if (= support_type 1)
			(setq support_string "1,1")
		)
		(if (= support_type 2)
			(setq support_string "0,1")
		)
		(if (= support_type 3)
			(setq support_string "1,0")
		)
		
		(write-line (strcat (rtos x1) "," (rtos y1) "," support_string) f)
		
		(setq counter (+ 1 counter))
	)	
	(write-line "END SUPPORTS" f)
	
	(close f)	 

	(setq my_command (strcat "python E:/Python_Scripts/moje/dsm3/Python/main.py " filename))
	(princ my_command)
	(command "._shell" my_command)

	(princ)
	
)


