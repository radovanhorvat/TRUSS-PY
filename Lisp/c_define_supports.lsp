(load "f_functions")
(vl-load-com)

(defun c:TP_define_supports( / support_layer support_type pt)

	(setq old_env_vars (env_get))
	(setvar "cmdecho" 0)
	(setvar "insunits" 0)
	
	(setq support_layer "TRUSSPY_supports")
	(command-s "._LAYER" "M" support_layer "C" "1" "" "")
	
	(setq support_type (getint "Enter support type (1-PXPY, 2-PY, 3-PX): "))
	
	(while t
		(setq pt (getpoint "Select point: "))
		(draw_support pt support_type)
		(vlax-ldata-put (entlast) "type" support_type)
	)
	
	(princ)
)


