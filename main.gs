SPREADSHEET_ID = "12y0ysclPzXTBi8N6I-Dn2pN1W6ug9Xihj_hvbw3_Ea0"

function doPost(e) {
  var sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName('master');
  
  if(!e) return;

  var payload = JSON.parse(e.postData['contents']);
  var members = payload.members;
  var player = members.filter(function(d){return d.isPlayer})[0];
  var winners = members.filter(function(d){return d.team === 'win'});
  var losers = members.filter(function(d){return d.team === 'lose'});
  
  row = [
    new Date(),
    player.udemae,        // ウデマエ
    payload.udemae_diff,  // ウデマエ増減
    payload.udemae_point, // ウデマエポイント
    player.kill,          // kill
    player.death,         // death
    winners[0].udemae,    // 勝ちチームウデマエ
    winners[1].udemae,
    winners[2].udemae,
    winners[3].udemae,
    losers[0].udemae,     // 負けチームウデマエ
    losers[1].udemae,
    losers[2].udemae,
    losers[3].udemae,
    payload.rule,         // ガチマッチルール
    payload.stage         // ステージ名
  ];
  
  sheet.appendRow(row);
  return ContentService.createTextOutput('').setMimeType(ContentService.MimeType.JSON);
  
}
