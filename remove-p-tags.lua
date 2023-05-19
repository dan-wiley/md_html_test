function removePTagsInLiBlocksRegex(element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    local content = pandoc.utils.stringify(element.content)
    content = content:gsub("<li>(.-)</li>", function(match)
      return "<li>" .. match:gsub("<p>(.-)</p>", "%1") .. "</li>"
    end)
    element.content = pandoc.read(content).blocks
  end
  return element
end

return {
  { Block = removePTagsInLiBlocksRegex }
}
