export default async function run(page, ui) {
  const result = await page.evaluate(() => {
    // Execute all scripts manually
    document.querySelectorAll('script').forEach(s => { try { (0, eval)(s.textContent); } catch (e) { } });
    // Now simulate full generation
    try {
    document.getElementById('trimestre').value = '1';
      cargarContenidos();
      const cbs = document.querySelectorAll('#areas-checkboxes input[type="checkbox"]:not([id^=all-])');
      cbs[0].checked = true;   // 1er contenido Comunicación
      cbs[12].checked = true;  // otro contenido
      generarPDC(false);
      const html = document.getElementById('contenido-pdc').innerHTML;
      const idx = html.indexOf('{contenido}');
      return {
        ok: true,
        len: html.length,
        leakCtx: idx === -1 ? 'sin leak' : html.substring(Math.max(0, idx - 150), idx + 50)
      };
    } catch (e) {
      return { ok: false, error: e.message, stack: (e.stack || '').split('\n').slice(0, 4).join(' | ') };
    }
  });
  return result;
}
