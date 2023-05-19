function removePTagsInLiBlocksRegex (element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    local content = pandoc.utils.stringify(element.content)
    content = content:gsub("<li><p>(.-)</p></li>", "<li>%1</li>")
    element.content = pandoc.read(content).blocks
  end
  return element
end

return {
  { Block = removePTagsInLiBlocksRegex }
}
