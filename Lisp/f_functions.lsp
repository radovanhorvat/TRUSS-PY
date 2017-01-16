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

(defun *error* (errmsg)
	(env_set old_env_vars)
)