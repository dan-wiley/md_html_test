function Div(el)
  if el.classes[1] == 'my-tag-class' then
    el.classes:insert(1, 'new-class')
  end
  return el
end
