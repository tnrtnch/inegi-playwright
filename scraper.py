from playwright.sync_api import sync_playwright
import json
import traceback


def clean(t):
    return " ".join(t.split())
  

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()


    try: 
        page.goto( 
            "https://www3.inegi.org.mx/sistemas/ci/relps/", 
            wait_until="load" 
        )


        # find iframe
        relps = next(
            f for f in page.frames
            if "relps" in f.url.lower()
        )



        # open full table
        relps.locator(
            "text=Ver total de proveedores sancionados"
        ).click()

        relps.wait_for_selector("(//tbody)[5]")

        rows = relps.locator("xpath=(//tbody)[5]/tr[position()>1]")

        for _ in range(20):
            if rows.count() > 0:
                break
            page.wait_for_timeout(500)

        total = rows.count()

        print(f"Total rows: {total}")

        merged = {}

        i = -1
        proveedor = "UNKNOWN"



        # waiting table
        relps.wait_for_selector("(//tbody)[5]")

        rows = relps.locator("xpath=(//tbody)[5]/tr[position()>1]")

        for _ in range(20):
            if rows.count() >= total - 1:
                break
            page.wait_for_timeout(500)

        print(f"Rows restored: {rows.count()}/{total}")


        for i in range(total):
            rows = relps.locator(
                "xpath=(//tbody)[5]/tr[position()>1]"
            )


            try:
                row = rows.nth(i)
                row.wait_for(state="visible", timeout=10000)
            except:
                print(f"Row {i+1} could not be restored")
                continue

            cols = row.locator("td")

            if cols.count() < 2:
                print(f"Row {i}: no column, skipping")
                continue

            proveedor = clean(cols.nth(0).text_content())

            # link element (no popup)
            link = row.locator("xpath=.//a[contains(@id,'gvProveedores')]")

            if link.count() == 0:
                continue

            link.first.scroll_into_view_if_needed()
            link.first.click(timeout=60000)

            # wait for the detail page to load
            relps.wait_for_selector(
                "xpath=//*[@id='cphContenido_gvHistorial']",
                timeout=60000
            )

            print("="*80)
            print(f"{i+1}/{total}")
            print(proveedor)

            numeros = set()

            rows_hist = relps.locator(
                "xpath=//*[@id='cphContenido_gvHistorial']/tbody/tr"
            )

  

            for h in range(1, rows_hist.count()):  
                try:
                    num = clean(rows_hist.nth(h).locator("td").nth(1).text_content())
                    if num:
                        numeros.add(num.strip())
                except:
                    pass


            if numeros:
                merged.setdefault(proveedor, set()).update(numeros)


            # come back
            relps.locator(
                "//*[contains(@id,'btnRegresar')]"
            ).click()

            relps.wait_for_selector(
                "text=Ver total de proveedores sancionados",
                timeout=60000
            )

            # show table
            relps.locator(
                "text=Ver total de proveedores sancionados"
            ).click()

            # waiting table
            relps.wait_for_selector(
                "(//tbody)[5]"
            )

            for _ in range(20):
                if rows.count() >= total - 1:
                    break

                page.wait_for_timeout(500) 

            print(f"Rows restored: {rows.count()}/{total}")

            print(f"END ITERATION {i+1}/{total}")

        print("FOR LOOP FINISHED")


        cleaned_data = [
            {
                "proveedor": proveedor,
                "numero": sorted(list(numeros))
            }
            for proveedor, numeros in merged.items()
        ]
    

        with open("relps_final.json", "w", encoding="utf-8") as f:
            json.dump(
                cleaned_data, 
                f,
                ensure_ascii=False, 
                indent=4
            )

        print(f"JSON records: {len(cleaned_data)}")
        print("\nFINISHED → relps_final.json")

    except Exception as e:
        print("=" * 80)
        print(f"ERROR at row {i+1}/{total}")
        print(f"Supplier: {proveedor}")
        traceback.print_exc()
        raise

    finally:
        browser.close()
