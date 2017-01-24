
(defun c:TP_define_supports( / old_env_vars ln_supports support_type pt)

	(setq old_env_vars (env_get))
	(setvar "cmdecho" 0)
	(setvar "insunits" 0)
	
	(setq ln_supports "TRUSSPY_supports")
	(command-s "._LAYER" "M" ln_supports "C" "1" "" "")
	
	(setq support_type (getint "Enter support type (1-PXPY, 2-PY, 3-PX): "))
	
	(while t
		(setq pt (getpoint "Select point: "))
		(draw_support pt support_type)
		(vlax-ldata-put (entlast) "type" support_type)
	)
	
	(princ)
)


