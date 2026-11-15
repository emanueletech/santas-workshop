# Santa's Workshop - CyberBrick Custom MPY Program. Runs at every power-on, no remote needed.
try:
    import bbl_product
    bbl_product.set_app_name("SANTA_WORKSHOP")
    bbl_product.set_app_version("02.04.00.00")
    del bbl_product
except Exception:
    pass
import main
main.main()
