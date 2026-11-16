const out = require('fs').readFileSync('out/html.json', 'utf8');
const exp = require('fs').readFileSync('C:/Users/User/AppData/Local/Temp/makefun-kits/markdown-render-speed-02-kit/practice/reference/expected.json', 'utf8');
const o = JSON.parse(out);
const e = JSON.parse(exp);
let match = 0;
for (let i = 0; i < o.length; i++) {
  const expectedHtml = e.cases[i]?.html;
  if (o[i] === expectedHtml) match++;
  else if (i < 5) console.log('Mismatch at', i, o[i]?.slice(0,100), '!=', expectedHtml?.slice(0,100));
}
console.log('Matched:', match, '/', o.length);
console.log('Expected cases:', e.cases.length);
