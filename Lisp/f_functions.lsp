; ENVIRONMENT VARIABLE GETTER AND SETTER
(defun env_get ( / old_layer old_osmode old_orthomode old_cmdecho old_attdia old_insunits old_dimzin output_list)
	; gets environment variables and returns
	; a list containing them
	(setq old_layer (getvar "clayer"))	
	(setq old_osmode (getvar "osmode"))	
	(setq old_orthomode (getvar "orthomode"))
	(setq old_cmdecho (getvar "cmdecho"))	
	(setq old_attdia (getvar "attdia"))  
	(setq old_insunits (getvar "insunits"))
	(setq old_dimzin (getvar "dimzin"))
	(setq output_list (list old_layer old_osmode old_orthomode old_cmdecho old_attdia old_insunits old_dimzin))
)

(defun env_set (input_list)
	; sets environment variable values to those in input_list
	(setvar "clayer" (nth 0 input_list))	
	(setvar "osmode" (nth 1 input_list))	
	(setvar "orthomode" (nth 2 input_list))		
	(setvar "cmdecho" (nth 3 input_list))	
	(setvar "attdia" (nth 4 input_list))
	(setvar "insunits" (nth 5 input_list))	
	(setvar "dimzin" (nth 6 input_list))
)

; SELECTION SET HANDLING
(defun apply_selset (sel / ed old_angle new_angle i entname len)
	; sel is a selection set
	(setq len (sslength sel))
	(setq i 0)
	(while (< i len)
		(setq entname (ssname sel i))
		(setq ed (entget entname))
		(ent_mod entname 300 "abcdef")
		(setq i (+ i 1))
	)
)

(defun ent_mod (entity_name code new_value / ed)
	(setq ed (entget entity_name))
	(setq ed
	  (subst (cons code new_value)
		(assoc code ed)           
		ed                      
	  )
	)
	(entmod ed)  
)

; SUPPORT BLOCK INSERTION
(defun draw_support (pt support_type / bs)
	; set block scale
	(setq bs 1)

	; block insertion
	(if (= support_type 1)
		(command-s "._INSERT" "TP_block_support_xy" pt bs bs 0)
	)
	(if (= support_type 2)
		(command-s "._INSERT" "TP_block_support_y" pt bs bs 0)
	)
	(if (= support_type 3)
		(command-s "._INSERT" "TP_block_support_x" pt bs bs 0)
	)
	
)

; LOAD BLOCK INSERTION
(defun draw_point_load (pt load_value load_type / load_value_str bs)

	; rounding off final elevation value
	(setvar "dimzin" 0)
	(setq load_value_str (rtos load_value 2 3))

	; get block scale
	(setq bs 1)

	; block insertion
	(if (= load_type 1)
		(command-s "._INSERT" "TP_block_load_x" pt bs bs 0 load_value_str)
	)
	(if (= load_type 2)
		(command-s "._INSERT" "TP_block_load_y" pt bs bs 0 load_value_str)
	)
	
	
)

;;;;;
(defun vl-getattributevalue ( blk tag )
    (setq tag (strcase tag))
    (vl-some '(lambda ( att ) (if (= tag (strcase (vla-get-tagstring att))) (vla-get-textstring att)))
        (vlax-invoke blk 'getattributes)
    )
)

; ERROR HANDLING
(defun *error* (errmsg)
	(env_set old_env_vars)
)