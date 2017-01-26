
(defun c:TP_define_loads ( / old_env_vars ln_loads load_type pt load_value)

	(setq old_env_vars (env_get))
	(setvar "cmdecho" 0)
	(setvar "insunits" 0)

	(setq ln_loads "TRUSSPY_loads")
	(command-s "._LAYER" "M" ln_loads "C" "3" "" "")
	
	(setq load_type (getint "Enter load type (1-Px, 2-Py): "))
	(setq load_value (getreal "\nEnter load value (kN): "))
	
	(while t
		(setq pt (getpoint "Select point: "))
		(draw_point_load pt load_value load_type)
		(vlax-ldata-put (entlast) "value" load_value)
	)
	
	(princ)
)

