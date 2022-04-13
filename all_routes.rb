routes = %w[
  1 2 3 4 5 6 7 8 8A 9
  X9 10 11 12 J14 15 18 19
  20 21 22 24 26 28 29 30
  31 34 35 36 37 39 43 44
  47 48 49 49B X49 50 51 52
  52A 53 53A 54 54A 54B 55 55A
  55N 56 57 59 60 62 62H 63
  63W 65 66 67 68 70 71 72
  73 74 75 76 77 78 79 80
  81 81W 82 84 85 85A 86 87
  88 90 91 92 93 94 95 96
  97 X98 100 103 106 108 111
  111A 112 115 119 120 121
  124 125 126 130 132 134
  135 136 143 146 147 148 151
  152 155 156 157 165 169 171
  172 192 201 205 206
]


require 'open-uri'
require 'active_support/all'
require 'json'

base_url = 'http://www.ctabustracker.com/bustime/api/v2'
all_stops = routes.map do |route|
  puts "Fetching bus ##{route}..."
  dir_params = {
    key: 'U529bPGQWxNMg85yPuDFm5nn3',
    format: 'json',
    rt: route
  }
  raw_dirs = open("#{base_url}/getdirections?#{dir_params.to_query}", &:read)
  directions = JSON.parse(raw_dirs)

  directions['bustime-response']['directions'].map do |dir|
    direction = dir['dir']
    puts "  for direction #{direction}"
    stops_params = {
      key: 'U529bPGQWxNMg85yPuDFm5nn3',
      format: 'json',
      rt: route,
      dir: direction
    }

    raw_stops = open("#{base_url}/getstops?#{stops_params.to_query}", &:read)
    stops = JSON.parse(raw_stops)
    stops['bustime-response']['stops'].map { |stop| stop['stpnm'] }
  end
end

def sanitize_stop_name(sname)
  sname = sname.downcase
  sname = sname.gsub('&', 'and')
  sname = sname.gsub(/\bn\.?\b/, 'north')
  sname = sname.gsub(/\bs\.?\b/, 'south')
  sname = sname.gsub(/\be\.?\b/, 'east')
  sname = sname.gsub(/\bw\.?\b/, 'west')
  sname = sname.gsub(/\bave\.?\b/, 'avenue')
  sname = sname.gsub(/\bblvd\.?\b/, 'boulevard')
  sname = sname.gsub(/\bctr\.?\b/, 'center')
  sname = sname.gsub(/\bst\./, 'saint')
  sname = sname.gsub(/-/, ' ')
end

File.open('all_routes.txt', 'w') do |file|
  all_stops.flatten.map(&method(:sanitize_stop_name)).uniq.sort.each do |stop|
    file.puts stop
    puts stop
  end
end
