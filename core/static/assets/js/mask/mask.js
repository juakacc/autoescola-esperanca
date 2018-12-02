$(document).ready(function () {
  // $('input[name=km_inicial]').mask('000.000.000.000.000,000', {reverse: true});
  // $('input[name=metrica_inicial]').mask("#,00");
  $('.numero').mask("#");
  $('.data').mask('00/00/0000');
  $('.placa_veiculo').mask('AAA-0000');
  $('.cpf').mask('000.000.000-00');
  // $('.cpf').attr('maxlength', 14);
  $('.telefone').mask('(00) 00000-0000');
  // $('input[name=qtd]').mask("#,00", {reverse: true, maxlength: false});
});
