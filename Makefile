all: ppds

ppds:
	LC_ALL=C ppdc -z drv/*

install:
	install -Dm 755 filter/rastertopm02.py $(DESTDIR)/usr/lib/cups/filter/rastertopm02
	install -Dm 755 backend/phomemo.py $(DESTDIR)/usr/lib/cups/backend/phomemo
	install -D drv/phomemo-m02pro.drv -t $(DESTDIR)/usr/share/cups/drv/
	install -D ppd/phomemo-m02pro.ppd.gz -t $(DESTDIR)/usr/share/cups/model/phomemo

	install -Dm 755 backend/canon.py $(DESTDIR)/usr/lib/cups/backend/canon
	install -D drv/canon-ivy2.drv -t $(DESTDIR)/usr/share/cups/drv/
	install -D ppd/canon-ivy2.ppd.gz -t $(DESTDIR)/usr/share/cups/model/canon
