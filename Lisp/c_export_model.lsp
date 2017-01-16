(load "f_functions")
(vl-load-com)

(defun c:TP_export_model( / selection counter entitydata entname layer_name pt_start pt_end E A
							x1 y1 x2 y2 element_list support_list data_bin ins_pt)


	(setq element_list (list))
	(setq support_list (list))
	
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
	
	(princ)
)


